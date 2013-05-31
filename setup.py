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

from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration

# simple setup
#
#from distutils.core import setup
#
#setup(name='pysa',
#      version='0.1a',
#      description='reverse a complete computer setup',
#      author='MadeiraCloud Ltd.',
#      author_email='pysa@mc2.io',
#      url='http://pysa.madeiracloud.com/',
#      packages=['pip'],
#      )

DISTNAME            = 'Pysa'
DESCRIPTION         = 'Reverse Engineer Server Configurations'
LONG_DESCRIPTION    = open('README.txt').read()
MAINTAINER          = 'Thibault BRONCHAIN - MadeiraCloud Ltd.'
MAINTAINER_EMAIL    = 'pysa@mc2.io'
URL                 = 'http://github.com/MadeiraCloud/pysa'
LICENSE             = 'LICENSE.txt'
DOWNLOAD_URL        = URL
VERSION             = '0.1.2a2'


def configuration(parent_package='', top_path=None, package_name=DISTNAME):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    config = Configuration(package_name, parent_package, top_path,
                           version = VERSION,
                           maintainer  = MAINTAINER,
                           maintainer_email = MAINTAINER_EMAIL,
                           description = DESCRIPTION,
                           license = LICENSE,
                           url = URL,
                           download_url = DOWNLOAD_URL,
                           long_description = LONG_DESCRIPTION)

    return config

if __name__ == "__main__":
    pkg = setuptools.find_packages()
    setup(configuration = configuration,
          install_requires = 'numpy',
          packages = pkg,
          include_package_data = True,
          zip_safe = True,
          classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: POSIX :: Linux',
            'Topic :: System'
            ]
          )
