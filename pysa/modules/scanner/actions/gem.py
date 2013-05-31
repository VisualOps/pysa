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
import re
import os

from base import scanner_base
import utils

class scanner_gem(scanner_base):

    def scan(self):
        """
        scan gem
        """
        logging.info('searching for Ruby gems')

        # Precompile a pattern for extracting the version of Ruby that was used
        # to install the gem.
        pattern = re.compile(r'gems/([^/]+)/gems')

        # Look for gems in all the typical places.  This is easier than looking
        # for `gem` commands, which may or may not be on `PATH`.
        for globname in ('/usr/lib/ruby/gems/*/gems',
                         '/usr/lib64/ruby/gems/*/gems',
                         '/usr/local/lib/ruby/gems/*/gems',
                         '/var/lib/gems/*/gems'):
            for dirname in glob.glob(globname):
                # The `ruby1.9.1` (really 1.9.2) package on Maverick begins
                # including RubyGems in the `ruby1.9.1` package and marks the
                # `rubygems1.9.1` package as virtual.  So for Maverick and
                # newer, the manager is actually `ruby1.9.1`.
                match = pattern.search(dirname)
                if '1.9.1' == match.group(1) and utils.rubygems_virtual():
                    manager = 'ruby{0}'.format(match.group(1))

                # Oneiric and RPM-based distros just have one RubyGems package.
                elif utils.rubygems_unversioned():
                    manager = 'rubygems'

                # Debian-based distros qualify the package name with the version
                # of Ruby it will use.
                else:
                    manager = 'rubygems{0}'.format(match.group(1))

                for entry in os.listdir(dirname):
                    try:
                        package, version = entry.rsplit('-', 1)

                    except ValueError:
                        logging.warning('skipping questionably named gem {0}'.
                                        format(entry))
                        continue

                    self.add_package(package, manager=manager, version=version, provider='gem')
