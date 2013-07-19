'''
Dictionnary converter for salt scripts generation

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
import hashlib

from pysa.tools import *
from pysa.config import *
from pysa.exception import *

from pysa.filter.filter import Filter


def handler_files_checksum(old, content):
    contents = ['content','key','source']
    c = None
    for c_name in contents:
        c = content.get(c_name)
        if c: break
    if not c: return None
    return "md5=%s"%(hashlib.md5(c).hexdigest())

def handler_actionkey_pkg(content):
    if (content.get('version') == 'latest') or not content.get('version'):
        content['version'] = None
        return 'latest'
    return 'installed'


# TODO: sources
# TODO: dependances

# define general sections
SECTION_EQ = {
#    'dirs'      : ACTION_ID+'file',
    'files'     : ACTION_ID+'file',
    'packages'  : {
        'key'   : 'provider',
        'apt'   : ACTION_ID+'pkg',
        'yum'   : ACTION_ID+'pkg',
        'rpm'   : ACTION_ID+'pkg',
        'php'   : ACTION_ID+'pecl',
        'pecl'  : ACTION_ID+'pecl',
        'pear'  : ACTION_ID+'pecl',
        'pip'   : ACTION_ID+'pip',
        'npm'   : ACTION_ID+'npm',
        'gem'   : ACTION_ID+'gem',
        },
    'services'  : ACTION_ID+'service',
    'crons'     : ACTION_ID+'cron',
    'groups'    : ACTION_ID+'group',
    'mounts'    : ACTION_ID+'mount',
    'hosts'     : ACTION_ID+'host',
    'repos'     : ACTION_ID+'file',
    'keys'      : ACTION_ID+'file',
    'users'     : ACTION_ID+'user',
#    'sources'   : {
#        'key'   : 'provider',
#        'git'   : ACTION_ID+'git',
#        'svn'   : ACTION_ID+'svn',
#        'hg'    : ACTION_ID+'hg',
#        }
    }

# avoided sections
AVOIDSEC_EQ = {
    'cron'      : ['environment', 'name', 'target'],
    'files'     : ['provider','recurse','recurselimit','source'],
    'groups'    : ['member','gid'],
    'hosts'     : ['target'],
    'mounts'    : ['atboot','size'],
    ACTION_ID+'pkg' : ['config_files','description','responsefile','provider','instance','category','platform','root','manager','vendor'],
    ACTION_ID+'pecl' : ['version','config_files','description','responsefile','provider','instance','category','platform','root','manager','vendor'],
    ACTION_ID+'gem' : ['version','config_files','description','responsefile','provider','instance','category','platform','root','manager','vendor'],
    ACTION_ID+'npm' : ['version','config_files','description','responsefile','provider','instance','category','platform','root','manager','vendor'],
    ACTION_ID+'pip' : ['version','config_files','description','responsefile','provider','instance','category','platform','root','manager','vendor'],
    'repos'     : ['provider','recurse','recurselimit','source'],
    'services'  : ['hasrestart','path','provider','binary','control','ensure','hasstatus','manifest','start','stop','restart'],
    'keys'      : ['target','host_aliases','type'],
    'users'     : ['uid', 'gid', 'expiry'],
}
# content add
CONTENTADD_EQ = {
    'files'     : {
        'makedirs'  : 'True',
        },
    'mounts'    : {
        'mkmnt'     : 'True',
        },
    'repos'     : {
        'makedirs'  : 'True',
        },
    'keys'      : {
        'source_hash' : 'md5',
        },
}
# key modifier
CONTENTKEY_EQ = {
    MAIN_SECTION : {
        },
    'crons'     : {
        'command'   : 'name',
        'monthday'  : 'daymonth',
        'weekday'   : 'dayweek',
        },
    'files'     : {
        'checksum'  : 'source_hash',
        'content'   : 'source',
        'owner'     : 'user',
        'path'      : 'name',
        'force'     : 'replace',
        },
    'hosts'     : {
        'name'      : 'names',
        'host_aliases' : 'names',
        },
    'mount'     : {
        'remounts'  : 'remount',
        'options'   : 'opts',
        },
    'repos' : {
        'checksum'  : 'source_hash',
        'content'   : 'source',
        'owner'     : 'user',
        'path'      : 'name',
        'force'     : 'replace',
        },
    'keys' : {
        'key'       : 'source',
        'path'      : 'name',
        },
    'users'     : {
        'group'     : 'gid',
        }
}
# val modifier (on key)
CONTENTVAL_EQ = {
    'files'     : {
        'source_hash' : [MAIN_SECTION,handler_files_checksum],
        },
    'repos'     : {
        'source_hash' : [MAIN_SECTION,handler_files_checksum],
        },
    'keys'     : {
        'source_hash' : [MAIN_SECTION,handler_files_checksum],
        },
}

# action key
ACTIONKEY_EQ = {
    'crons'     : 'present',
    'files'     : 'managed',
    'groups'    : 'present',
    'hosts'     : 'present',
    'mounts'    : 'mounted',
    ACTION_ID+'pkg' : handler_actionkey_pkg,
    ACTION_ID+'pecl' : 'installed',
    ACTION_ID+'gem' : 'installed',
    ACTION_ID+'npm' : 'installed',
    ACTION_ID+'pip' : 'installed',
    'repos'     : 'managed',
    'service'   : 'running',
    'keys'      : 'managed',
    'users'     : 'present',
}

# Append sections
APPSEC_EQ = {
}


class SaltConverter():
    def __init__(self, minput, filters=None):
        self.__output = {}
        self.__input = dict(minput.items())
        self.__filter = Filter(filters)

    # main method
    @GeneralException
    def run(self):
        Tools.l(INFO, "running", 'run', self)

        #empty imput
        if not self.__input:
            Tools.l(ERR, "empty input", 'run', self)
            return {}

        self.__curent_state = None

        # convert
        self.__generate_classes(self.__input)

        Tools.l(INFO, "complete", 'run', self)
        return self.__output

    # processing on values
    @GeneralException
    def __process_values(self, manifest, name, key, val):
        if type(val) is int:
            val = "%s" % (val)
        elif (type(val) is not str) or (not val):
            return val
        if (manifest in APPSEC_EQ) and (key == APPSEC_EQ[manifest][0]):
            val = APPSEC_EQ[manifest][1] + val
        return self.__filter.item_replace(manifest, key, val, name)

    # processing on data
    @GeneralException
    def __process_data(self, data, manifest, name):
        Tools.l(INFO, "processing data", 'process_data', self)
        sec_key = (self.__curent_state if type(SECTION_EQ[manifest]) is dict else manifest)

        # modifications
        kcontent = Tools.list_merging(AVOIDSEC_EQ.get(MAIN_SECTION), AVOIDSEC_EQ.get(sec_key))
        for key in kcontent:
            if key in data:
                data[key] = None
        kcontent = Tools.s_dict_merging(CONTENTADD_EQ.get(MAIN_SECTION), CONTENTADD_EQ.get(sec_key))
        for key in kcontent:
            data[key] = kcontent[key]
        kcontent = Tools.s_dict_merging(CONTENTKEY_EQ.get(MAIN_SECTION), CONTENTKEY_EQ.get(sec_key))
        for key in kcontent:
            if key in data:
                data[kcontent[key]] = Tools.merge_string_list(data.get(kcontent[key]), data.pop(key))
        kcontent = Tools.s_dict_merging(CONTENTVAL_EQ.get(MAIN_SECTION), CONTENTVAL_EQ.get(sec_key))
        for key in kcontent:
            if key in data:
                if (data[key] == kcontent[key][0]) or (kcontent[key][0] == MAIN_SECTION):
                    if type(kcontent[key][1]) is str:
                        data[key] = kcontent[key][1]
                    else:
                        data[key] = kcontent[key][1](data[key], data)

        # set action key
        kcontent = ACTIONKEY_EQ.get(sec_key)
        if type(kcontent) is str:
            data[kcontent] = MAIN_SECTION
        elif kcontent:
            data[kcontent(data)] = MAIN_SECTION

        # main loop
        for key in data:
            if type(data[key]) is list:
                store = []
                for d in data[key]:
                    store.append(self.__process_values(manifest, name, key, d))
                data[key] = store
            else:
                data[key] = self.__process_values(manifest, name, key, data[key])

        return data

    # ganaration method
    @GeneralException
    def __generate_classes(self, data):
        for manifest in sorted(data):
            if manifest not in SECTION_EQ:
                Tools.l(INFO, "Ignored unknown class %s" % (manifest), 'generate_classes', self)
                continue
            Tools.l(INFO, "creating manifest %s" % (manifest), 'generate_classes', self)
            for name in sorted(data[manifest]):
                if type(SECTION_EQ[manifest]) is dict:
                    ref = data[manifest][name].get(SECTION_EQ[manifest]['key'])
                    if not ref:
                        Tools.l(ERR, "Reference key not found %s" % (SECTION_EQ[manifest]['key']), 'generate_classes', self)
                        continue
                    state = SECTION_EQ[manifest].get(ref)
                    if not state:
                        Tools.l(ERR, "State not found ref %s, manifest %s"%(ref,manifest), 'generate_classes', self)
                        continue
                else:
                    state = SECTION_EQ.get(manifest)
                    if not state:
                        Tools.l(ERR, "State not found manifest %s"%(manifest), 'generate_classes', self)
                        continue
                if (manifest == 'packages'):
                    data[manifest][name] = self.__filter.update_package(data[manifest][name], name, 'latest')
                self.__output.setdefault(manifest, {})
                self.__output[manifest].setdefault(state, {})
                self.__curent_state = state
                self.__output[manifest][state][name] = self.__process_data(data[manifest][name], manifest, name)
