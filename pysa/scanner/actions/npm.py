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

import re
import logging

from pysa.scanner.actions.base import scanner_base


class scanner_npm(scanner_base):
    def scan(self):
        """
        scan apt
        """
        logging.info('searching for npm packages')

        # Precompile a pattern for parsing the output of `npm list -g`.
        pattern = re.compile(r'^\S+ (\S+)@(\S+)$')

        lines = self.subprocess(['npm', 'ls', '-g'])    # only list global packages
        for line in lines:
            match = pattern.match(line.rstrip())
            if match is None:
                continue
            package, version = match.group(1), match.group(2)
            manager='nodejs'

            self.add_package(package, manager=manager, version=version, provider='npm')
