'''
Created on 2013-04-19

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
import subprocess

from pysa.scanner.actions.base import scanner_base


class scanner_process(scanner_base):

    def scan(self):
        """
        scan process
        """
        logging.info('searching for process')

        self.get_processes()

    def get_processes(self):
        """
        get all the process info
        """

        try:
            p = subprocess.Popen(['-c', 'ps -eo pid,fuser,s,pcpu,pmem,comm,ppid'], shell=True, stdout=subprocess.PIPE)

            first = True
            for line in p.stdout:
                if first:   # ignore the headline
                    first = False
                    continue

                lst = line.strip().split()

                # check data completeness
                nonlst = [info for info in lst if info is None]
                if len(nonlst)>0: continue

                self.add_proc(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5], lst[6])

        except OSError:
            return

    def get_accounts(self):
        """
        parse the system accounts config file('/etc/passwd')
        """

        try:
            data = open('/etc/passwd').read()
            for line in data:
                att = line.strip().split(':')
                if att[0] is not None and att[2] is not None:
                    self.add_accout(att[2], att[0])
        except IOError:
            return False

        return True

    @property
    def accounts(self):
        if accounts not in self:
            self.accounts = {}

        return self.accounts

    def add_accout(self, uid, name):
        if uid not in self.accounts:
            self.accounts[uid] = name
