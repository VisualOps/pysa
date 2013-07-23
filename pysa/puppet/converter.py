'''
Dictionnary converter for puppet scripts generation

    pysa - reverse a complete computer setup
    Copyright (C) 2013  MadeiraCloud Ltd.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

@author: Thibault BRONCHAIN
'''

import re
import copy

from pysa.tools import *
from pysa.config import *
from pysa.exception import *

from pysa.filter.filter import Filter


# define _order section

# list of ordered sections
ORDERED_LIST_EQ = ['sources']

# general modifiers
GLOBAL_SEC_EQ = {
    'Exec'      : ACTION_ID+'Exec',
    'exec'      : ACTION_ID+'exec',
    'order'     : ACTION_ID+'order',
    'require'   : SINGLE_SEC+'require'
}

# define _Exec section
GLOBAL_EXEC_EQ = {
    'path'      : '/usr/bin:/bin:/usr/sbin:/sbin'
}

# define _exec section
EXEC_EQ = {
    'apt'   : 'apt-get update',
    'yum'   : '/usr/sbin/yum-complete-transaction',
    'pip'   : 'easy_install pip',
    }

# define general sections
SECTION_EQ = {
    'dirs'      : ACTION_ID+'file',
    'files'     : ACTION_ID+'file',
    'packages'  : ACTION_ID+'package',
    'services'  : ACTION_ID+'service',
    'crons'     : ACTION_ID+'cron',
    'groups'    : ACTION_ID+'group',
    'mounts'    : ACTION_ID+'mount',
    'hosts'     : ACTION_ID+'host',
    'repos'     : ACTION_ID+'file',
    'keys'      : ACTION_ID+'file',
    'users'     : ACTION_ID+'user',
    'sources'   : ACTION_ID+'vcsrepo'
    }
SECTION_CALL_EQ = dict([(key,SECTION_EQ[key].capitalize()) for key in SECTION_EQ])

# define subsclasses equivalency
SUBCLASS_EQ = {
    'packages'  : {
        MAIN_SECTION : 'provider',
        'order'   : [
            ['apt', 'yum', 'rpm'],
            ['npm', 'pecl', 'pear', 'pip', 'gem']
            ]
        }
}

# add 'require' instruction
REQUIRE_EQ = [
    SUBCLASS_EQ['packages']['order']
    ]

# key modifier
CONTENTKEY_EQ = {
    MAIN_SECTION     : {
        'version'   : 'ensure',
        'key'       : 'content'
        },
    'sources'   : {
        'scm'       : 'provider'
        },
    'users'     : {
        'group'     : 'gid'
        }
}

# val modifier (on key)
CONTENTVAL_EQ = {
    'packages'  : {
        'provider'  : ['php', 'pear']
        }
}

# content add
CONTENTADD_EQ = {
    'sources'   : {
        'ensure'    : 'present'
        },
    'groups'    : {
        'ensure'    : 'present'
        }
}

# avoided sections
AVOIDSEC_EQ = {
    'mounts'    : ['size'],
    'packages'  : ['manager', 'config_files'],
    'sources'   : ['mode', 'password', 'branch', 'name', 'key'],
    'groups'    : ['gid'],
    'users'     : ['uid', 'gid'],
    'repos'     : ['provider'],
}

# Append sections
APPSEC_EQ = {
    'crons'     : ['environment', 'PATH=']
}

class PuppetConverter():
    def __init__(self, minput, filters = None):
        self.__output = {}
        self.__input = copy.deepcopy(minput)
        self.__filter = Filter(filters)
        self.__prev_obj = None

    # main method
    @GeneralException
    def run(self):
        Tools.l(INFO, "running", 'run', self)

        #empty imput
        if not self.__input:
            Tools.l(ERR, "empty input", 'run', self)
            return {}

        # convert
        self.__generate_classes(self.__input)

        # add exceptions
        if GLOBAL_EXEC_EQ:
            self.__add_global_exec()

        Tools.l(INFO, "complete", 'run', self)
        return self.__output

    # generate global exec
    @GeneralException
    def __add_global_exec(self):
        Tools.l(INFO, "adding Exec section", 'add_global_exec', self)
        self.__output[GLOBAL_SEC_EQ['Exec']] = {MAIN_SECTION : {}}
        for key in GLOBAL_EXEC_EQ:
            Tools.l(INFO, "adding key %s" % (key), 'add_global_exec', self)
            self.__output[GLOBAL_SEC_EQ['Exec']][MAIN_SECTION][key] = self.__process_values('', 'Exec', key, GLOBAL_EXEC_EQ[key])

    # generate sub execs
    @GeneralException
    def __add_top_class(self, key):
        c = {}
        for order in REQUIRE_EQ:
            if key in order[0]: break
            elif key in order[1]:
                req = []
                for r in order[0]:
                    req.append(r)
                if req:
                    c = Tools.dict_merging(c, {
                            GLOBAL_SEC_EQ['require'] : req
                            })
        if key in EXEC_EQ:
            Tools.l(INFO, "adding exec section for %s" % (key), 'add_exec', self)
            c = Tools.dict_merging(c, {
                    GLOBAL_SEC_EQ['exec'] : {
                        EXEC_EQ[key] : GLOBAL_EXEC_EQ
                        }
                    })
        return c

    # processing on values
    @GeneralException
    def __process_values(self, gclass, name, key, val):
        if type(val) is int:
            val = "%s" % (val)
        elif (type(val) is not str) or (not val):
            return val
        if (gclass in APPSEC_EQ) and (key == APPSEC_EQ[gclass][0]):
            val = APPSEC_EQ[gclass][1] + val
        return self.__filter.item_replace(gclass, key, val, name)


    # processing on data
    @GeneralException
    def __process_data(self, input, gclass, name, cur_class):
        Tools.l(INFO, "processing data", 'process_data', self)
        # modifications
        kcontent = Tools.list_merging(AVOIDSEC_EQ.get(MAIN_SECTION), AVOIDSEC_EQ.get(gclass))
        for key in kcontent:
            if key in input:
                input[key] = None
        kcontent = Tools.s_dict_merging(CONTENTADD_EQ.get(MAIN_SECTION), CONTENTADD_EQ.get(gclass), False)
        for key in kcontent:
            input[key] = kcontent[key]
        kcontent = Tools.s_dict_merging(CONTENTKEY_EQ.get(MAIN_SECTION), CONTENTKEY_EQ.get(gclass), False)
        for key in kcontent:
            if key in input:
                input[kcontent[key]] = input.pop(key)
        kcontent = Tools.s_dict_merging(CONTENTVAL_EQ.get(MAIN_SECTION), CONTENTVAL_EQ.get(gclass), False)
        for key in kcontent:
            if key in input:
                if input[key] == kcontent[key][0]:
                    input[key] = kcontent[key][1]

        # exec dependency
        if cur_class in EXEC_EQ:
            input['require'] = Tools.dict_merging(input.get('require'), {
                    GLOBAL_SEC_EQ['exec'][len(ACTION_ID):].capitalize() : [
                        EXEC_EQ[cur_class]
                        ]
                    })

        # main loop
        for key in input:
            if type(input[key]) is list:
                store = []
                for d in input[key]:
                    store.append(self.__process_values(gclass, name, key, d))
                input[key] = store
            else:
                input[key] = self.__process_values(gclass, name, key, input[key])
        return input

    # processing on section
    @GeneralException
    def __process_sec(self, data, gclass, name, cur_class):
        Tools.l(INFO, "creating section %s" % (SECTION_EQ[gclass]), 'process_sec', self)
        if (SECTION_EQ[gclass] == ACTION_ID+'package'):
            data[gclass][name] = self.__filter.update_package(data[gclass][name], name, 'latest')
        return self.__process_data(data[gclass][name], gclass, name, cur_class)

    # class generation
    @GeneralException
    def __generate_classes(self, data):
        for gclass in data:
            if gclass not in SECTION_EQ:
                Tools.l(INFO, "Ignored unknown class %s" % (gclass), 'generate_classes', self)
                continue
            Tools.l(INFO, "creating class %s" % (gclass), 'generate_classes', self)
            self.__prev_obj = None
            self.__output[gclass] = self.__add_top_class(gclass)
            for name in sorted(data[gclass]):
                if gclass in SUBCLASS_EQ:
                    subkey = data[gclass][name][SUBCLASS_EQ[gclass][MAIN_SECTION]]
                    Tools.l(INFO, "creating sub class %s" % (subkey), 'generate_classes', self)
                    self.__output[gclass].setdefault(subkey, self.__add_top_class(subkey))
                    self.__output[gclass][subkey].setdefault(SECTION_EQ[gclass], {})
                    self.__output[gclass][subkey][SECTION_EQ[gclass]][name] = self.__process_sec(data, gclass, name, subkey)
                else:
                    self.__output[gclass].setdefault(SECTION_EQ[gclass], {})
                    self.__output[gclass][SECTION_EQ[gclass]][name] = self.__process_sec(data, gclass, name, gclass)
                self.__prev_obj = name
