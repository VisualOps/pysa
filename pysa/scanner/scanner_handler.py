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

from pysa.scanner.actions.file import ScannerFile
from pysa.scanner.actions.gem import ScannerGem
from pysa.scanner.actions.npm import ScannerNpm
from pysa.scanner.actions.php import ScannerPhp
from pysa.scanner.actions.pypi import ScannerPypi
from pysa.scanner.actions.service import ScannerService
from pysa.scanner.actions.host import ScannerHost
from pysa.scanner.actions.mount import ScannerMount
from pysa.scanner.actions.cron import ScannerCron
from pysa.scanner.actions.sshkey import ScannerKey
from pysa.scanner.actions.user import ScannerUser
from pysa.scanner.actions.group import ScannerGroup
from pysa.scanner.actions.package import ScannerPackage
from pysa.scanner.actions.source import ScannerSource
from pysa.scanner.actions.repository import ScannerRepo
from pysa.scanner.actions.process import ScannerProcess
from pysa.scanner.actions.base import ScannerBase
#------------------------------------------------------------

class ScannerHandler():

    # stay aware of the order
    handler = {
                "file"      : ScannerFile,
                "gem"       : ScannerGem,
                "npm"       : ScannerNpm,
                "php"       : ScannerPhp,
                "pypi"      : ScannerPypi,
                "service"   : ScannerService,
                "host"      : ScannerHost,
                'user'      : ScannerUser,
                'group'     : ScannerGroup,
                'mount'     : ScannerMount,
                'cron'      : ScannerCron,
                'key'       : ScannerKey,
                'package'   : ScannerPackage,
                'source'    : ScannerSource,
                'repository': ScannerRepo,
                'process'   : ScannerProcess
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
        s = ScannerBase(
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
    scanner = ScannerHandler(filters)
    return scanner.scan()
