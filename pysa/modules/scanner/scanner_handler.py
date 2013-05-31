'''
Created on 2013-3-28

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

@author: Ken
'''
#------------------------------------------------------------
import logging
import time
from actions.file import scanner_file
from actions.gem import scanner_gem
from actions.npm import scanner_npm
from actions.php import scanner_php
from actions.pypi import scanner_pypi
from actions.service import scanner_service
from actions.host import scanner_host
from actions.mount import scanner_mount
from actions.cron import scanner_cron
from actions.sshkey import scanner_key
from actions.user import scanner_user
from actions.group import scanner_group
from actions.package import scanner_package
from actions.source import scanner_source
from actions.repository import scanner_repo
from actions.process import scanner_process
from actions.base import scanner_base
#------------------------------------------------------------

class scanner_handler():

    # stay aware of the order
    handler = {
                "file"      : scanner_file,
                "gem"       : scanner_gem,
                "npm"       : scanner_npm,
                "php"       : scanner_php,
                "pypi"      : scanner_pypi,
                "service"   : scanner_service,
                "host"      : scanner_host,
                'user'      : scanner_user,
                'group'     : scanner_group,
                'mount'     : scanner_mount,
                'cron'      : scanner_cron,
                'key'       : scanner_key,
                'package'   : scanner_package,
                'source'    : scanner_source,
                'repository': scanner_repo,
                'process'   : scanner_process
               }



    def __init__(self, rules):
        self.resources  =   {
                                'packages'  :   {},
                                'files'     :   {},
                                'crons'     :   {},
                                'groups'    :   {},
                                'mounts'    :   {},
                                'hosts'     :   {},
                                'repos'     :   {},
                                'services'  :   {},
                                'keys'      :   {},
                                'users'     :   {},
                                'ips'       :   [],
                                'sources'   :   {},
                                'proces'    :   {}

                             }

        self.rules = rules if rules else {}

    def scan(self):

        # init the base scanner
        s = scanner_base(
                self.resources['packages'],
                self.resources['files'],
                self.resources['crons'],
                self.resources['groups'],
                self.resources['mounts'],
                self.resources['hosts'],
                self.resources['repos'],
                self.resources['services'],
                self.resources['keys'],
                self.resources['users'],
                self.resources['ips'],
                self.resources['sources'],
                self.resources['proces']
        )
        # init the filter rules
        s.init_filter(self.rules)

        for scanner_key in self.handler.keys():
            # ignore the discard resources
            if 'discard' in self.rules and '_resources' in self.rules['discard'] and scanner_key in self.rules['discard']['_resources']: continue

            # time begin
            time_begin = time.time()

            # log
            logging.info('ScannerHandler.scan(): Scanning Module %s, time begin at %s ' % (scanner_key, time_begin))

            # scan according to different modules
            try:
                s.__class__ = self.handler[scanner_key]
                
                s.scan()

            except Exception, e:
                logging.error('ScannerHandler.scan(): %s Error message, %s' % (scanner_key,str(e)))

            # time end
            time_consume = time.time() - time_begin
            logging.info('ScannerHandler.scan(): Scanning Module %s, time consume %s ' % (scanner_key, time_consume))

        return self.resources

def module_scan(filters = None):
    scanner = scanner_handler(filters)
    return scanner.scan()
