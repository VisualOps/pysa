'''
Created on 2013-04-18

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

import os
import logging

from pysa.scanner.actions.utils import *
from pysa.scanner.actions.base import scanner_base


class scanner_repo(scanner_base):

    def scan(self):
        """
        scan for repository config files
        """
        logging.info('searching for repository config files')

        if os.path.exists('/etc/yum.repos.d'):
            self.scan_yum()
        elif os.path.exists('/etc/apt'):
            self.scan_apt()

    def scan_yum(self):
        """
        scan yum repo config files
        """

        for dirpath, dirnames, files in os.walk('/etc/yum.repos.d'):
            for file in files:
                root, ext = os.path.splitext(file)
                if ext!='.repo': continue

                self.addfile(os.path.join(dirpath, file), 'yum')

    def scan_apt(self):
        """
        scan apt repo config files
        """

        try:
            with open('/etc/apt/sources.list'): self.addfile('/etc/apt/sources.list', 'apt')
        except IOError:
            return

        if os.path.exists('/etc/apt/sources.list.d'):
            for dirpath, dirnames, files in os.walk('/etc/apt/sources.list.d'):
                for file in files:
                    root, ext = os.path.splitext(file)
                    if ext!='.list': continue

                    self.addfile(os.path.join(dirpath, file), 'apt')


    # add per config file
    def addfile(self, pathname, prov):
        # only plane text file
        if valid_txtfile(pathname) == False:
            return

        # get owner, group and mode
        s = get_stat(pathname)

        # read the config file's content
        c = get_content(pathname)

        # add the config file:
        # checksum, content, group, mode, owner, path, force=False, provider=None,
        # recurse=None, recurselimit=None, source=None
        self.add_repo('md5', c, s[0], s[1], s[2], pathname, provider=prov)
