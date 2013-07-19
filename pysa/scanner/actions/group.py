'''
Created on 2013-4-4

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

import logging
import grp

from pysa.scanner.actions.base import ScannerBase


class ScannerGroup(ScannerBase):
    
    def scan(self):
        for g in grp.getgrall():
            name, password, gid, member = g
            self.add_group(name=name, gid=gid, member=member)
