'''
Output container

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

# output container
class output():
    def __init__(self):
        self.main = ''
        self.c = {}

    @GeneralException
    def add_dict(self, output, default = ''):
        self.c[output] = default

    @GeneralException
    def add(self, output, content):
        if output:
            self.c[output] += content
        else:
            self.main += content

    @GeneralException
    def dump(self, manifest_name = ''):
        return (self.c[manifest_name] if manifest_name else self.main)

    @GeneralException
    def list(self):
        l = ([''] if self.main else [])
        for i in self.c:
            l.append(i)
        return l

    @GeneralException
    def mod(self, content, output = ''):
        if output:
            self.c[output] = content
        else:
            self.main = content        
