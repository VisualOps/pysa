'''
List dependencies for all resources

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


SCM_EQ = {
    'git' : ['git', 'git-all'],
    'svn' : ['subversion'],
    'hg'  : ['mercurial'],
}

SELF_ORDER_EQ = {
    'dirs'          : 'path',
    'sources'       : 'path',
    'mounts'        : 'name',
    }

PRIOR = ['sources']

BASED_ON_FIELD      = "BASED_ON_FIELD"
SELF_ORDER          = "SELF_ORDER"
GET_MOUNT_FROM_PATH = "GET_MOUNT_FROM_PATH"
GET_BASE_PATH       = "GET_BASE_PATH"
GET_PKG_FROM_SCM    = "GET_PKG_FROM_SCM"
PACKAGE_MANAGER     = "PACKAGE_MANAGER"


class Dependencies:
    def __init__(self, module):
        exec "from %s.converter import SECTION_CALL_EQ"%module
        exec "from %s.objects import *"%module
        self.__obj_maker = OBJ_MAKER
        self.__deps = DEPENDENCIES
        self.__calls = SECTION_CALL_EQ
        self.__handler = {
            BASED_ON_FIELD      : self.__based_on_field,
            SELF_ORDER          : self.__self_order,
            GET_MOUNT_FROM_PATH : self.__get_mount_from_path,
            GET_BASE_PATH       : self.__get_base_path,
            GET_PKG_FROM_SCM    : self.__get_pkg_from_scm,
            PACKAGE_MANAGER     : self.__package_manager,
            }
        self.__data = None
        self.__add_obj = {}

    @GeneralException
    def run(self, data):
        self.__data = copy.deepcopy(data)
        Tools.l(INFO, "running dependency cycle generation", 'run', self)
        for c in self.__data:
            if ((c not in self.__deps)
                or (c not in self.__calls)): continue
            for obj_name in self.__data[c]:
                obj = self.__data[c][obj_name]
                for dep_name in PRIOR:
                    if ((dep_name not in self.__data)
                        or (dep_name not in self.__calls)): continue
                    elif dep_name in self.__deps[c]:
                        self.__parse_dep(c, obj_name, obj, dep_name)
                for dep_name in self.__deps[c]:
                    if ((dep_name not in self.__data)
                        or (dep_name not in self.__calls)
                        or (dep_name in PRIOR)): continue
                    else: self.__parse_dep(c, obj_name, obj, dep_name)
        if self.__add_obj: self.__data = Tools.dict_merging(self.__add_obj, self.__data)
        Tools.l(INFO, "dependency cycle generated", 'run', self)
        return self.__data

    @GeneralException
    def __parse_dep(self, c, obj_name, obj, dep_name):
        dep = self.__deps[c][dep_name]
        if type(dep) is str:
            obj['require'] = Tools.dict_merging(obj.get('require'), {
                    dep : [dep_name]
                    })
        elif type(dep) is list:
            res = self.__handler[dep[0]](obj, dep_name, dep[1])
            if res:
                section_dep = self.__calls[dep_name]
                if type(self.__calls[dep_name]) is dict:
                    target_obj = (res[0] if type(res) is list else res)
                    tmp_data = (Tools.dict_merging(self.__add_obj, self.__data) if self.__add_obj else self.__data)
                    section_obj = tmp_data[dep_name].get(target_obj)
                    if not section_obj:
                        Tools.l(ERR, "Target object missing %s.%s"%(dep_name,target_obj), 'parse_dep', self)
                        return
                    section_key = section_obj.get(self.__calls[dep_name]['key'])
                    if not section_key:
                        Tools.l(ERR, "Section key missing for %s"%(dep_name), 'parse_dep', self)
                        return
                    section_dep = self.__calls[dep_name].get(section_key)
                    if not section_dep:
                        Tools.l(ERR, "Wrong section key %s[%s]"%(dep_name,section_key), 'parse_dep', self)
                        return
                obj['require'] = Tools.dict_merging(obj.get('require'), {
                        section_dep[len(ACTION_ID):] : res
                        })

    @GeneralException
    def __self_order(self, object, gclass, args):
        ref = object.get(args['field'])
        data = self.__data[gclass]
        if not data: return None
        res = None
        for key in sorted(data, key=lambda x: data[x][args['field']]):
            name = data[key][args['field']]
            if re.match(name, ref) and (ref != name):
                res = key
        if gclass == 'sources' and self.__data.get('dirs') and res:
            dirs = dict(self.__data['dirs'].items())
            for dir in dirs:
                comp = Tools.path_basename(ref)
                if dirs[dir]['path'] == comp:
                    self.__data['dirs'].pop(dir)
        return res

    @GeneralException
    def __get_mount_from_path(self, object, gclass, args):
        path = object.get(args['field'])
        mounts = self.__data['mounts']
        if not mounts: return None
        res = None
        for key in sorted(mounts, key=lambda x: mounts[x]['name']):
            name = mounts[key]['name']
            if re.match(name, path):
                res = key
        return res

    @GeneralException
    def __get_pkg_from_scm(self, object, gclass, args):
        scm = object.get(args['field'])
        return (SCM_EQ.get(scm) if scm else None)

    @GeneralException
    def __get_base_path(self, object, gclass, args):
        path = object.get(args['field'])
        return (Tools.path_basename(path) if path else None)

    @GeneralException
    def __based_on_field(self, object, gclass, args):
        if not args.get('field') or not args.get('key'):
            return []
        res = []
        v_field = (self.__handler[args['field'][0]](object, gclass, args['field'][1])
                   if type(args['field']) is list
                   else object.get(args['field']))
        if v_field:
            for obj_name in self.__data[gclass]:
                v_key = (args['key'][0](object, gclass, obj_name, args['key'][1])
                         if type(args['key']) is list
                         else self.__data[gclass][obj_name].get(args['key']))
                if (((type(v_field) is list) and (v_key in v_field))
                    or ((type(v_key) is list) and (v_field in v_key))
                    or (v_key == v_field)):
                    res.append(obj_name)
        return res

    @GeneralException
    def __package_manager(self, object, gclass, args):
        if not args.get('field'): return []
        provider = object.get(args['field'])
        managers = Config.managers_eq
        platform = Config.platform
        if provider and platform and managers and (provider in managers):
            package = managers[provider]
            if package not in self.__data['packages'] and managers['_autoadd']:
                self.__add_obj.setdefault(gclass, {})
                self.__add_obj[gclass][package] = self.__obj_maker['manager'](package, platform)
                return [package]
            elif package in self.__data['packages']:
                return [package]
        return []
