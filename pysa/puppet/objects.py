'''
Puppet Objects

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

from pysa.exception import *

from pysa.scanner.actions.utils import get_stat
from pysa.dependencies import *

class PuppetObjects():
    @staticmethod
    def puppet_file_dir_obj(dr):
        # get group, mode and owner
        #s = get_stat(dr)
        #DEBUG
        s = ('root', oct(0777), 'root')
        #/DEBUG
        return {
            'path'      : dr,
            'ensure'    : 'directory',
            'name'      : dr,
            'group'     : s[0],
            'mode'      : s[1],
            'owner'     : s[2],
            }

    @staticmethod
    def puppet_pkg_manager_obj(package, provider):
        return {
            'name'      : package,
            'provider'  : provider,
            'version'   : 'latest',
            }


OBJ_MAKER = {
    'file' : PuppetObjects.puppet_file_dir_obj,
    'manager' : PuppetObjects.puppet_pkg_manager_obj,
    }

DEPENDENCIES = {
    'hosts'     : {},
    'mounts'    : {
        'hosts'     : 'Class',
        'mounts'    : [
            BASED_ON_FIELD, {
                'field' : [SELF_ORDER, {
                        'field'     : 'name',
                        }],
                'key'   : 'name',
                }
            ],
        },
    'groups'    : {
        'hosts'     : 'Class',
        },
    'users'     : {
        'hosts'     : 'Class',
        'groups'    : [
            BASED_ON_FIELD, {
                'field' : 'group',
                'key'   : 'name',
                }
            ],
        },
    'dirs'      : {
        'hosts'     : 'Class',
        'dirs'    : [
            BASED_ON_FIELD, {
                'field' : [SELF_ORDER, {
                        'field'     : 'path',
                        }],
                'key'   : 'path',
                }
            ],
        'groups'    : [
            BASED_ON_FIELD, {
                'field' : 'group',
                'key'   : 'name',
                }
            ],
        'users'     : [
            BASED_ON_FIELD, {
                'field' : 'owner',
                'key'   : 'name',
                }
            ],
        'mounts'    : [
            BASED_ON_FIELD, {
                'field' : [GET_MOUNT_FROM_PATH, {
                        'field'     : 'path',
                        }],
                'key'   : 'device',
                }
            ],
        },
    'keys'      : {
        'hosts'     : 'Class',
        'groups'    : [
            BASED_ON_FIELD, {
                'field' : 'group',
                'key'   : 'name',
                }
            ],
        'users'     : [
            BASED_ON_FIELD, {
                'field' : 'owner',
                'key'   : 'name',
                }
            ],
        'dirs'      : [
            BASED_ON_FIELD, {
                'field' : [GET_BASE_PATH, {
                        'field'     : 'path',
                        }],
                'key'   : 'path',
                }
            ],
        },
    'repos'     : {
        'hosts'     : 'Class',
        'groups'    : [
            BASED_ON_FIELD, {
                'field' : 'group',
                'key'   : 'name',
                }
            ],
        'users'     : [
            BASED_ON_FIELD, {
                'field' : 'owner',
                'key'   : 'name',
                }
            ],
        'dirs'      : [
            BASED_ON_FIELD, {
                'field' : [GET_BASE_PATH, {
                        'field'     : 'path',
                        }],
                'key'   : 'path',
                }
            ],
        },
    'packages'  : {
        'hosts'     : 'Class',
        'repos'     : [
            BASED_ON_FIELD, {
                'field' : 'provider',
                'key'   : 'provider',
                }
            ],
        'dirs'      : [
            BASED_ON_FIELD, {
                'field' : [GET_BASE_PATH, {
                        'field'     : 'path',
                        }],
                'key'   : 'path',
                }
            ],
        },
    'files'     : {
        'hosts'     : 'Class',
        'groups'    : [
            BASED_ON_FIELD, {
                'field' : 'group',
                'key'   : 'name',
                }
            ],
        'users'     : [
            BASED_ON_FIELD, {
                'field' : 'owner',
                'key'   : 'name',
                }
            ],
        'dirs'      : [
            BASED_ON_FIELD, {
                'field' : [GET_BASE_PATH, {
                        'field'     : 'path',
                        }],
                'key'   : 'path',
                }
            ],
        'packages'  : [
            BASED_ON_FIELD, {
                'field' : 'path',
                'key'   : 'config_files',
                }
            ],
        },
    'crons'     : {
        'hosts'     : 'Class',
        'users'     : [
            BASED_ON_FIELD, {
                'field' : 'user',
                'key'   : 'name',
                }
            ],
        },
    'sources'   : {
        'hosts'     : 'Class',
        'sources'   : [
            BASED_ON_FIELD, {
                'field' : [SELF_ORDER, {
                        'field'     : 'path',
                        }],
                'key'   : 'path',
                }
            ],
        'groups'    : [
            BASED_ON_FIELD, {
                'field' : 'group',
                'key'   : 'name',
                }
            ],
        'users'     : [
            BASED_ON_FIELD, {
                'field' : 'owner',
                'key'   : 'name',
                }
            ],
        'dirs'      : [
            BASED_ON_FIELD, {
                'field' : [GET_BASE_PATH, {
                        'field'     : 'path',
                        }],
                'key'   : 'path',
                }
            ],
        'keys'      : [
            BASED_ON_FIELD, {
                'field' : 'key',
                'key'   : 'name',
                }
            ],
        'packages'  : [
            BASED_ON_FIELD, {
                'field' : [GET_PKG_FROM_SCM, {
                        'field'     : 'scm',
                        }],
                'key'   : 'name',
                }
            ],
        },
    'services'  : {
        'files'     : 'Class',
        },
    }
