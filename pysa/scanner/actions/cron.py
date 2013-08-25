'''
Scan cron files

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

@author: Michael
'''

import logging
import os

from pysa.scanner.actions.base import ScannerBase


class ScannerCron(ScannerBase):
    def scan(self):

        users = self.get_users()
        res = self.subprocess(['crontab', '-l'])
        for line in res:
            # ignore the comment lines
            if line.strip().startswith("#"): continue

            ary = line.split()
            if ary[5] in users.keys():
                paths = os.path.split(ary[6])
                self.add_cron(
                              name=paths[1],
                              command=" ".join(ary[6:]),
                              environment=paths[0],
                              user=ary[5],
                              minute=ary[0],
                              hour=ary[1],
                              monthday=ary[2],
                              month=ary[3],
                              weekday=ary[4]
                              )
            else:
                paths = os.path.split(ary[5])
                self.add_cron(
                              name=paths[1],
                              command=" ".join(ary[5:]),
                              environment=paths[0],
                              minute=ary[0],
                              hour=ary[1],
                              monthday=ary[2],
                              month=ary[3],
                              weekday=ary[4]
                              )
