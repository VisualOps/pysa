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

from common.exception import *

from modules.scanner.actions.utils import get_stat

class puppet_objects():
    @staticmethod
    def puppet_file_dir_obj(dr):
        # get group, mode and owner
        s = get_stat(dr)
        #s = ('root', oct(0777), 'root')
        return {
            'path'      : dr,
            'ensure'    : 'directory',
            'name'      : dr,
            'group'     : s[0],
            'mode'      : s[1],
            'owner'     : s[2],
            }

PUPPET_OBJ_MAKER = {
    'file' : puppet_objects.puppet_file_dir_obj
    }
