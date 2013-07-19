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
import pwd
import grp

from pysa.scanner.actions.base import ScannerBase


class ScannerUser(ScannerBase):
    def scan(self):
        for p in pwd.getpwall():
            name, password, uid, gid, gecos, home, shell = p

            groups = [] 
            # get the secondary groups
            for gr in grp.getgrall():
                gr_name, gr_pwd, gr_gid, gr_mem = gr
                # check whether the main group
                if gid == gr_gid:   
                    group = gr_name
                    continue
                # check whether the group member
                if name in gr_mem:
                    groups.append(gr_name)

            if group is None or not group: continue

            self.add_user(name=name, uid=uid, gid=gid, group=group, groups=groups, shell=shell, home=home)
