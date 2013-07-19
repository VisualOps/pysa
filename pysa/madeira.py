'''
Export output to Madeira account

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
from pysa.tools import *

# TODO
# export data to madeira account
class Madeira():
    def __init__(self, user, user_id, output, module):
        self.__user = user
        self.__user_id = user_id
        self.__output = output
        self.__module = module

    # send data to Madeira account
    def send(self):
        Tools.l(ERR, "ABORTING: not yet implemented", func.__name__, self)
