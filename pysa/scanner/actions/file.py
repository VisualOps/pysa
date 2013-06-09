'''
Created on 2013-3-31

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
import re
import logging

from pysa.config import *
from pysa.scanner.actions.utils import *
from pysa.scanner.actions.base import scanner_base


class scanner_file(scanner_base):

    suf_list = ['.conf', '.cfg', '.ini']
    
    def scan(self):
        """
        scan config files
        """

        logging.info('searching for config files')

        # scan the system directories
        self.scandir(config.files_path)
        
    # scan directory and add config files
    def scandir(self, pathdir): 
        # Visit every file in pathdir except those on the exclusion list above.
        pathdirs = re.split(":", pathdir)
        for p in pathdirs:
            for dirpath, dirnames, filenames in os.walk(p, followlinks=True):
                for filename in filenames:
                    self.addfile(os.path.join(dirpath, filename))

    # add per config file
    def addfile(self, pathname):
        # only plane text file
        if valid_txtfile(pathname) == False:     
            return

#        # only include above suffix config file
#        suf = os.path.splitext(pathname)[1]
#        if suf is None or suf not in self.suf_list:
#            return

        # get owner, group and mode
        s = get_stat(pathname)
        
        # read the config file's content
        c = get_content(pathname)

        # add the config file:
        # checksum, content, group, mode, owner, path, force=False, provider=None, 
        # recurse=None, recurselimit=None, source=None
        self.add_file('md5', c, s[0], s[1], s[2], pathname)
