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

from pysa.tools import *
from pysa.config import *
from pysa.exception import *

from pysa.puppet.puppet_converter import SECTION_EQ

SCM_EQ = {
    'git' : ['git', 'git-all'],
    'svn' : ['subversion'],
    'hg'  : ['mercurial'],
}

SELF_ORDER = {
    'dirs'          : 'path',
    'sources'       : 'path',
    'mounts'        : 'name',
    }

PRIOR = ['sources']

class dependencies:
    def __init__(self, data=None):
        # define dependencies
        self.__deps = {
            'hosts'     : {},
            'mounts'    : {
                'hosts'     : None,
                'mounts'    : [
                    self.__based_on_field, {
                        'field' : [self.__self_order, {
                                'field'     : 'name',
                                }],
                        'key'   : 'name',
                        }
                    ],
                },
            'groups'    : {
                'hosts'     : None,
                },
            'users'     : {
                'hosts'     : None,
                'groups'    : [
                    self.__based_on_field, {
                        'field' : 'group',
                        'key'   : 'name',
                        }
                    ],
                },
            'dirs'      : {
                'hosts'     : None,
                'dirs'    : [
                    self.__based_on_field, {
                        'field' : [self.__self_order, {
                                'field'     : 'path',
                                }],
                        'key'   : 'path',
                        }
                    ],
                'groups'    : [
                    self.__based_on_field, {
                        'field' : 'group',
                        'key'   : 'name',
                        }
                    ],
                'users'     : [
                    self.__based_on_field, {
                        'field' : 'owner',
                        'key'   : 'name',
                        }
                    ],
                'mounts'    : [
                    self.__based_on_field, {
                        'field' : [self.__get_mount_from_path, {
                                'field'     : 'path',
                                }],
                        'key'   : 'device',
                        }
                    ],
                },
            'keys'      : {
                'hosts'     : None,
                'groups'    : [
                    self.__based_on_field, {
                        'field' : 'group',
                        'key'   : 'name',
                        }
                    ],
                'users'     : [
                    self.__based_on_field, {
                        'field' : 'owner',
                        'key'   : 'name',
                        }
                    ],
                'dirs'      : [
                    self.__based_on_field, {
                        'field' : [self.__get_base_path, {
                                'field'     : 'path',
                                }],
                        'key'   : 'path',
                        }
                    ],
                },
            'repos'     : {
                'hosts'     : None,
                'groups'    : [
                    self.__based_on_field, {
                        'field' : 'group',
                        'key'   : 'name',
                        }
                    ],
                'users'     : [
                    self.__based_on_field, {
                        'field' : 'owner',
                        'key'   : 'name',
                        }
                    ],
                'dirs'      : [
                    self.__based_on_field, {
                        'field' : [self.__get_base_path, {
                                'field'     : 'path',
                                }],
                        'key'   : 'path',
                        }
                    ],
                },
            'packages'  : {
                'hosts'     : None,
                'repos'     : [
                    self.__based_on_field, {
                        'field' : 'provider',
                        'key'   : 'provider',
                        }
                    ],
                'dirs'      : [
                    self.__based_on_field, {
                        'field' : [self.__get_base_path, {
                                'field'     : 'path',
                                }],
                        'key'   : 'path',
                        }
                    ],
                },
            'files'     : {
                'hosts'     : None,
                'groups'    : [
                    self.__based_on_field, {
                        'field' : 'group',
                        'key'   : 'name',
                        }
                    ],
                'users'     : [
                    self.__based_on_field, {
                        'field' : 'owner',
                        'key'   : 'name',
                        }
                    ],
                'dirs'      : [
                    self.__based_on_field, {
                        'field' : [self.__get_base_path, {
                                'field'     : 'path',
                                }],
                        'key'   : 'path',
                        }
                    ],
                'packages'  : [
                    self.__based_on_field, {
                        'field' : 'path',
                        'key'   : 'config_files',
                        }
                    ],
                },
            'crons'     : {
                'hosts'     : None,
                'users'     : [
                    self.__based_on_field, {
                        'field' : 'user',
                        'key'   : 'name',
                        }
                    ],
                },
            'sources'   : {
                'hosts'     : None,
                'sources'   : [
                    self.__based_on_field, {
                        'field' : [self.__self_order, {
                                'field'     : 'path',
                                }],
                        'key'   : 'path',
                        }
                    ],
                'groups'    : [
                    self.__based_on_field, {
                        'field' : 'group',
                        'key'   : 'name',
                        }
                    ],
                'users'     : [
                    self.__based_on_field, {
                        'field' : 'owner',
                        'key'   : 'name',
                        }
                    ],
                'dirs'      : [
                    self.__based_on_field, {
                        'field' : [self.__get_base_path, {
                                'field'     : 'path',
                                }],
                        'key'   : 'path',
                        }
                    ],
                'keys'      : [
                    self.__based_on_field, {
                        'field' : 'key',
                        'key'   : 'name',
                        }
                    ],
                'packages'  : [
                    self.__based_on_field, {
                        'field' : [self.__get_pkg_from_scm, {
                                'field'     : 'scm',
                                }],
                        'key'   : 'name',
                        }
                    ],
                },
            'services'  : {
                'files'     : None,
                },
            }

        self.__data = data


    @general_exception
    def run(self, data = None):
        tools.l(INFO, "running dependency cycle generation", 'run', self)
        if data:
            self.__data = data
        for c in self.__data:
            if c not in self.__deps: continue
            for obj_name in self.__data[c]:
                obj = self.__data[c][obj_name]
                for dep_name in PRIOR:
                    if dep_name in self.__deps[c]:
                        self.__parse_dep(c, obj_name, obj, dep_name)
                for dep_name in self.__deps[c]:
                    if dep_name in PRIOR: continue
                    else: self.__parse_dep(c, obj_name, obj, dep_name)
        tools.l(INFO, "dependency cycle generated", 'run', self)

    @general_exception
    def __parse_dep(self, c, obj_name, obj, dep_name):
        dep = self.__deps[c][dep_name]
        if not dep:
            obj['require'] = tools.dict_merging(obj.get('require'), {
                    'Class' : [dep_name]
                    })
        elif type(dep) is list:
            res = dep[0](obj, dep_name, dep[1])
            if res:
                obj['require'] = tools.dict_merging(obj.get('require'), {
                        SECTION_EQ[dep_name][len(VOID_EQ):].capitalize() : res
                        })

    @general_exception
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
                comp = tools.path_basename(ref)
                if dirs[dir]['path'] == comp:
                    self.__data['dirs'].pop(dir)
        return res

    @general_exception
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

    @general_exception
    def __get_pkg_from_scm(self, object, gclass, args):
        scm = object.get(args['field'])
        return (SCM_EQ.get(scm) if scm else None)

    @general_exception
    def __get_base_path(self, object, gclass, args):
        path = object.get(args['field'])
        return (tools.path_basename(path) if path else None)

    @general_exception
    def __based_on_field(self, object, gclass, args):
        if not args.get('field') or not args.get('key'):
            return []
        res = []
        v_field = (args['field'][0](object, gclass, args['field'][1])
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
