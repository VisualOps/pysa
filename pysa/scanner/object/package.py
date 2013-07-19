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


class Package(ObjectBase):
    
    def __init__(self, name, files=None, description=None, version=None, responsefile=None, provider=None,
                 instance=None, category=None, platform=None, manager=None, root=None, vendor=None):
        self.name = name
        self.config_files = files
        self.description = description
        self.version = version
        self.responsefile = responsefile
        self.provider = provider
        self.instance = instance
        self.category = category
        self.platform = platform
        self.root   =   root
        self.manager = manager
        self.vendor = vendor
