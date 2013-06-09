#!/usr/bin/env python
'''
Installation script for setup from pip

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

import os
import sys
import setuptools

from distutils.core import setup

DISTNAME            = 'Pysa'
VERSION             = '0.2.0a7'
DESCRIPTION         = 'Reverse Engineer Server Configurations'
LONG_DESCRIPTION    = open('README.txt').read()
MAINTAINER          = 'Thibault BRONCHAIN - MadeiraCloud Ltd.'
MAINTAINER_EMAIL    = 'pysa@mc2.io'
LICENSE             = 'LICENSE.txt'
URL                 = 'http://pypi.python.org/pypi/Pysa/'
DOWNLOAD_URL        = 'http://pypi.python.org/packages/source/P/Pysa/Pysa-'+VERSION+'.tar.gz'
#PACKAGES            = ['pysa']
#PACKAGE_DIR         = {'pysa': 'pysa'}
SCRIPTS             = ['bin/pysa2puppet', 'bin/pysa']

if __name__ == "__main__":
    pkg = setuptools.find_packages()
    print pkg
    setup(name=DISTNAME,
          version=VERSION,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          url=URL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          download_url=DOWNLOAD_URL,
          license=LICENSE,
          packages = pkg,
#          packages=PACKAGES,
#          package_dir=PACKAGE_DIR,
          scripts=SCRIPTS,
          classifiers = [
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: POSIX :: Linux',
            'Topic :: System',
            ]
          )
