'''
Created on 2013-3-29

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
import re

from pysa.scanner.actions.utils import *
from pysa.scanner.actions.base import ScannerBase


class ScannerPhp(ScannerBase):
    def scan(self):
        """
        scan php
        """
        logging.info('searching for PEAR/PECL packages')

        # Precompile a pattern for parsing the output of `{pear,pecl} list`.
        pattern = re.compile(r'^([0-9a-zA-Z_]+)\s+([0-9][0-9a-zA-Z\.-]*)\s')

        # PEAR packages are managed by `php-pear` (obviously).  PECL packages
        # are managed by `php5-dev` because they require development headers
        # (less obvious but still makes sense).
        if lsb_release_codename() is None:
            pecl_manager = 'php-devel'
        else:
            pecl_manager = 'php5-dev'
        for manager, progname in (('php-pear', 'pear'),
                                  (pecl_manager, 'pecl')):

            lines = self.subprocess([progname, 'list'])
            if lines==None:
                return
                
            for line in lines:
                match = pattern.match(line)
                if match is None:
                    continue
                package, version = match.group(1), match.group(2)
                
                self.add_package(package, manager=manager, version=version, provider=progname)
