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

from common.tools import *
from common.config import *
from common.exception import *

from modules.filter.filter import filter


# define _order section
ORDER_EQ = {
    VOID_EQ     : [
                   'mounts',
                   'dirs',
                   'groups',
                   'users',
                   'hosts',
                   'keys',
                   'repos',
                   'packages',
                   'files',
                   'crons',
                   'sources',
                   'services',
                   ]
    }

# list of ordered sections
ORDERED_LIST_EQ = ['sources']

# general modifiers
GLOBAL_SEC_EQ = {
    'Exec'      : VOID_EQ+'Exec',
    'exec'      : VOID_EQ+'exec',
    'order'     : VOID_EQ+'order',
    'require'   : SINGLE_EQ+'require'
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
    'dirs'      : VOID_EQ+'file',
    'files'     : VOID_EQ+'file',
    'packages'  : VOID_EQ+'package',
    'services'  : VOID_EQ+'service',
    'crons'     : VOID_EQ+'cron',
    'groups'    : VOID_EQ+'group',
    'mounts'    : VOID_EQ+'mount',
    'hosts'     : VOID_EQ+'host',
    'repos'     : VOID_EQ+'file',
    'keys'      : VOID_EQ+'file',
    'users'     : VOID_EQ+'user',
    'sources'   : VOID_EQ+'vcsrepo'
}

# define subsclasses equivalency
SUBCLASS_EQ = {
    'packages'  : {
        VOID_EQ   : 'provider',
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
    VOID_EQ     : {
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

# content modifier (on lists)
#CONTENTLVAL_EQ = {
#    'files'             : ['before','File'],
#    'config_files'      : ['before','File']
#}

# avoided sections
AVOIDSEC_EQ = {
    'mounts'    : ['size'],
    'packages'  : ['manager', 'config_files'],
    'sources'   : ['mode', 'password', 'branch', 'name', 'key'], #check key
    'groups'    : ['gid'],
    'users'     : ['uid', 'gid'],
    'repos'     : ['provider'],
}

# Append sections
APPSEC_EQ = {
    'crons'     : ['environment', 'PATH=']
}

class puppet_converter():
    def __init__(self, minput, filters = None):
        self.__output = {}
        self.__input = minput
        self.__filter = filter(filters)
        self.__prev_obj = None

    # main method
    @general_exception
    def run(self):
        tools.l(INFO, "running", 'run', self)

        #empty imput
        if not self.__input:
            tools.l(ERR, "empty input", 'run', self)
            return {}

        # convert
        self.__generate_classes(self.__input)

        # add exceptions
        if GLOBAL_EXEC_EQ:
            self.__add_global_exec()
#        if ORDER_EQ:
#            self.__add_order()

        tools.l(INFO, "complete", 'run', self)
        return self.__output

    # generate global exec
    @general_exception
    def __add_global_exec(self, sec_name='Exec'):
        tools.l(INFO, "adding Exec section", 'add_global_exec', self)
        self.__output[GLOBAL_SEC_EQ[sec_name]] = {VOID_EQ : {}}
        for key in GLOBAL_EXEC_EQ:
            tools.l(INFO, "adding key %s" % (key), 'add_global_exec', self)
            self.__output[GLOBAL_SEC_EQ[sec_name]][VOID_EQ][key] = self.__process_values('', sec_name, key, GLOBAL_EXEC_EQ[key])

    # generate sub execs
    @general_exception
    def __add_top_class(self, key):
        c = {}
        for order in REQUIRE_EQ:
            if key in order[0]: break
            elif key in order[1]:
                req = []
                for r in order[0]:
                    req.append(r)
                if req:
                    c = tools.dict_merging(c, {
                            GLOBAL_SEC_EQ['require'] : req
                            })
        if key in EXEC_EQ:
            tools.l(INFO, "adding exec section for %s" % (key), 'add_exec', self)
            c = tools.dict_merging(c, {
                    GLOBAL_SEC_EQ['exec'] : {
                        EXEC_EQ[key] : GLOBAL_EXEC_EQ
                        }
                    })
            
        return c

#    # generate order
#    @general_exception
#    def __append_order(self, src, dst, sec_name='order'):
#        order = []
#        for sec in src:
#            if sec in dst:
#                order.append(sec)
#        if order:
#            dst[GLOBAL_SEC_EQ[sec_name]] = order
#        else:
#            tools.l(INFO, "no pertinent order", 'append_order', self)
#
#    # order generation
#    @general_exception
#    def __add_order(self):
#        for key in ORDER_EQ:
#            if key == VOID_EQ:
#                tools.l(INFO, "adding order for main section", 'add_order', self)
#                self.__append_order(ORDER_EQ[key], self.__output)
#            else:
#                tools.l(INFO, "adding order for %s" % (key), 'add_order', self)
#                self.__append_order(ORDER_EQ[key], self.__output[key])

    # processing on values
    @general_exception
    def __process_values(self, gclass, name, key, val):
        if type(val) is int:
            val = "%s" % (val)
        elif (type(val) is not str) or (not val):
            return val
        if (gclass in APPSEC_EQ) and (key == APPSEC_EQ[gclass][0]):
            val = APPSEC_EQ[gclass][1] + val
        return self.__filter.item_replace(gclass, key, val, name)


    # processing on data
    @general_exception
    def __process_data(self, input, gclass, name, cur_class):
        tools.l(INFO, "processing data", 'process_data', self)
        # modifications
        kcontent = tools.list_merging(AVOIDSEC_EQ.get(VOID_EQ), AVOIDSEC_EQ.get(gclass))
        for key in kcontent:
            if key in input:
                input[key] = None
        kcontent = tools.s_dict_merging(CONTENTADD_EQ.get(VOID_EQ), CONTENTADD_EQ.get(gclass))
        for key in kcontent:
            input[key] = kcontent[key]
        kcontent = tools.s_dict_merging(CONTENTKEY_EQ.get(VOID_EQ), CONTENTKEY_EQ.get(gclass))
        for key in kcontent:
            if key in input:
                input[kcontent[key]] = input.pop(key)
        kcontent = tools.s_dict_merging(CONTENTVAL_EQ.get(VOID_EQ), CONTENTVAL_EQ.get(gclass))
        for key in kcontent:
            if key in input:
                if input[key] == kcontent[key][0]:
                    input[key] = kcontent[key][1]

        # exec dependency
        if cur_class in EXEC_EQ:
            input['require'] = tools.dict_merging(input.get('require'), {
                    GLOBAL_SEC_EQ['exec'][len(VOID_EQ):].capitalize() : [
                        EXEC_EQ[cur_class]
                        ]
                    })

#        # ordering condition
#        if (gclass in ORDERED_LIST_EQ) and self.__prev_obj != None:
#            input['require'] = tools.dict_merging(input.get('require'), {
#                    SECTION_EQ[gclass][len(VOID_EQ):].capitalize() : [
#                        self.__prev_obj
#                        ]
#                    })

        # main loop
        for key in input:
            if type(input[key]) is list:
                store = []
                for d in input[key]:
                    store.append(self.__process_values(gclass, name, key, d))
#                if key in CONTENTLVAL_EQ:
#                    input.pop(key)
#                    input[CONTENTLVAL_EQ[key][0]] = {
#                        CONTENTLVAL_EQ[key][1] : store
#                        }
#                else:
                input[key] = store
            else:
                input[key] = self.__process_values(gclass, name, key, input[key])
        return input

    # processing on section
    @general_exception
    def __process_sec(self, data, gclass, name, cur_class):
        tools.l(INFO, "creating section %s" % (SECTION_EQ[gclass]), 'process_sec', self)
        if (SECTION_EQ[gclass] == VOID_EQ+'package'):
            data[gclass][name] = self.__filter.update_package(data[gclass][name], name, 'latest')
        return self.__process_data(data[gclass][name], gclass, name, cur_class)

    # class generation
    @general_exception
    def __generate_classes(self, data):
        for gclass in data:
            if gclass not in SECTION_EQ:
                tools.l(INFO, "Ignored unknown class %s" % (gclass), 'generate_classes', self)
                continue
            tools.l(INFO, "creating class %s" % (gclass), 'generate_classes', self)
            self.__prev_obj = None
            self.__output[gclass] = self.__add_top_class(gclass)
            for name in sorted(data[gclass]):
                if gclass in SUBCLASS_EQ:
                    subkey = data[gclass][name][SUBCLASS_EQ[gclass][VOID_EQ]]
                    tools.l(INFO, "creating sub class %s" % (subkey), 'generate_classes', self)
                    self.__output[gclass].setdefault(subkey, self.__add_top_class(subkey))
                    self.__output[gclass][subkey].setdefault(SECTION_EQ[gclass], {})
                    self.__output[gclass][subkey][SECTION_EQ[gclass]][name] = self.__process_sec(data, gclass, name, subkey)
                else:
                    self.__output[gclass].setdefault(SECTION_EQ[gclass], {})
                    self.__output[gclass][SECTION_EQ[gclass]][name] = self.__process_sec(data, gclass, name, gclass)
                self.__prev_obj = name
