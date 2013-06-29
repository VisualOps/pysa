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
import shutil
import subprocess
import setuptools

from distutils.core import setup
from distutils.command.install import install
from distutils.command.sdist import sdist

DISTNAME            = 'Pysa'
VERSION             = '0.2.3a'
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

def abspath(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

class pysa_install(install):
    user_options = install.user_options

    def initialize_options(self):
        install.initialize_options(self)

    def run(self):
        install.run(self)

        man_dir = abspath("./docs/man/")
        output = subprocess.Popen(
            [os.path.join(man_dir, "pysa_man.sh")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=man_dir,
            env=dict({"PREFIX": self.prefix}, **dict(os.environ))
            ).communicate()[0]
        print output

class pysa_sdist(sdist):
    def run(self):
        sdist.run(self)

if __name__ == "__main__":
    pkg = setuptools.find_packages()
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
            'Topic :: System'
            ],
          cmdclass={"install": pysa_install, "sdist": pysa_sdist}
          )
