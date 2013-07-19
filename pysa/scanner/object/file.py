'''
Created on 2013-3-27

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

from pysa.scanner.object.object_base import ObjectBase


class File(ObjectBase):
    
    def __init__(self, checksum, content, group, mode, owner, path, force=False, provider=None, recurse=None, recurselimit=None, source=None):
        self.checksum   =   checksum
        self.content    =   content
        self.group      =   group
        self.mode       =   mode
        self.owner      =   owner
        self.path       =   path
        self.force      =   force
        self.provider   =   provider
        self.recurse    =   recurse
        self.recurselimit   =   recurselimit
        self.source     =   source
    
