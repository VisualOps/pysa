'''
Created on 2013-3-28

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

from pysa.scanner.object.object_base import object_base


class service(object_base):   
    
    def __init__(self, enable, hasrestart, name, path, \
                 provider=None, binary=None, control=None, ensure=None, \
                 hasstatus=None, manifest=None, start=None, stop=None, restart=None):
        self.enable = enable
        self.hasrestart = hasrestart
        self.name = name
        self.path = path
        self.provider = provider
        self.binary = binary
        self.control = control,
        self.ensure = ensure
        self.hasstatus = hasstatus
        self.manifest = manifest
        self.start = start
        self.stop = stop
        self.restart = restart
        
        
        
