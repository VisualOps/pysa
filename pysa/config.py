'''
Global configuration

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

from ConfigParser import SafeConfigParser

from pysa.tools import *
from pysa.exception import *


# define who is a file
FILE_CLASS      = ['keys', 'repos', 'files']
# order
ORDER_LIST = [
    'hosts',
    'mounts',
    'groups',
    'users',
    'dirs',
    'keys',
    'repos',
    'packages',
    'files',
    'crons',
    'sources',
    'services',
    ]
# null objects (avoid 0)
NULL            = ['', {}, [], None]
# build-ins
VOID_EQ         = '_'
ACTION_ID       = '_'
MAIN_SECTION    = '_'
SINGLE_SEC      = '__'

# configuration class
class Config():

    # default values
    c = {
        'files' : {
            'path' : '/etc:/root/.ssh'
            },
        'keys' : {
            'path' : 'root/.ssh'
            },
        'hosts' : {
            'path' : '/etc/hosts'
            },
        'managers' : {
            '_autoadd' : True,
            'pear' : 'php-pear',
            'pecl' : 'php-pear',
            'pip'  : 'python-pip',
            'npm'  : 'npm',
            'gem'  : 'rubygems',
            },
        }
    files_path = c['files']['path']
    scan_host = c['hosts']['path']
    key_path = c['keys']['path']
    managers_eq = c['managers']
    platform = None

    # edit default values if config file
    def __init__(self, path=None):
        if not path: return
        self.__filename = path
        self.__parse_config()

    # parse config file
    @GeneralException
    def __parse_config(self):
        parser = SafeConfigParser()
        parser.read(self.__filename)
        for name in parser.sections():
            config.c.setdefault(name, {})
            for key, value in parser.items(name):
                if   value == "True" : value = True
                elif value == "False": value = False
                config.c[name][key] = value
