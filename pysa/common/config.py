'''
Created on 2013-4-17

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

@author: Ken
'''

# define who is a file
NULL            = ['', {}, [], None]
FILE_CLASS      = ['keys', 'repos', 'files']
VOID_EQ         = '_'
SINGLE_EQ       = VOID_EQ+VOID_EQ

# configuration class (not used for now)
class config():
    
    files_path = '/etc:/root/.ssh'
    scan_host = '/etc/hosts'
    key_path = '/root/.ssh'
    
    def __init__(self):
        pass
