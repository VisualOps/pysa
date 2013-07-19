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

import glob
import logging
import os
import re
import subprocess

from pysa.scanner.actions.base import ScannerBase


# Precompile a pattern to extract the manager from a pathname.
PATTERN_MANAGER = re.compile(r'lib/(python[^/]*)/(dist|site)-packages')

# Precompile patterns for differentiating between packages built by
# `easy_install` and packages built by `pip`.
PATTERN_EGG = re.compile(r'\.egg$')
PATTERN_EGGINFO = re.compile(r'\.egg-info$')

# Precompile a pattern for extracting package names and version numbers.
PATTERN = re.compile(r'^([^-]+)-([^-]+).*\.egg(-info)?$')

class ScannerPypi(ScannerBase):

    def scan(self):
        """
        scan pypi
        """
        logging.info('searching for Python packages')

        # Look for packages in the typical places.
        globnames = ['/usr/lib/python*/dist-packages',
                     '/usr/lib/python*/site-packages',
                     '/usr/local/lib/python*/dist-packages',
                     '/usr/local/lib/python*/site-packages']
        virtualenv = os.getenv('VIRTUAL_ENV')
        if virtualenv is not None:
            globnames.extend(['{0}/lib/python*/dist-packages'.format(virtualenv),
                              '{0}/lib/python*/dist-packages'.format(virtualenv)])
        for globname in globnames:
            for dirname in glob.glob(globname):
                manager = PATTERN_MANAGER.search(dirname).group(1)
                for entry in os.listdir(dirname):
                    match = PATTERN.match(entry)
                    if match is None:
                        continue
                    package, version = match.group(1, 2)
                    
                    pathname = os.path.join(dirname, entry)

                    # Symbolic links indicate this is actually a system package
                    # that injects files into the PYTHONPATH.
                    if os.path.islink(pathname): continue

                    # check pathname
                    if not os.path.isdir(pathname):
                        pathname = os.path.join(dirname, package)
                        if not os.path.exists(pathname): continue

                    # installed via `easy_install`.
                    if PATTERN_EGG.search(entry):
                        self.add_package(package, manager='python', version=version, provider='pip')

                    # installed via `pip`.
                    elif PATTERN_EGGINFO.search(entry):
                        self.add_package(package, manager='pip', version=version, provider='pip')                    
