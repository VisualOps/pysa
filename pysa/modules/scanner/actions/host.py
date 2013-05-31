'''
Created on 2013-04-03

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
import os

from common.config import *
from base import scanner_base
import utils


class scanner_host(scanner_base):

    def scan(self):
        """
        scan host:
        parse the host config file (usually /etc/hosts)
        """
        logging.info('searching for hosts')
        hostlst = self.parse_hostfile()

        if len(hostlst)<=0:
            return

        for dict in hostlst:
            self.add_host(ip=dict['ip'], name=dict['name'],
                target=dict['target'], host_aliases=dict['host_aliases'])

    def parse_hostfile(self):
        hostfile = config.scan_host

        try:
            hosts = []
            for line in open(hostfile):
                # ignore blank line
                if not line.strip(): continue
                # ignore comment line
                if line.strip().startswith("#"): continue

                itemlst = line.strip().split()
                ip = re.search( r'[0-9]+(?:\.[0-9]+){3}', itemlst[0] )
                if ip==None:
                    continue
                
                aliases = []
                if len(itemlst)>=3:
                    for i in range(2, len(itemlst)-1):
                        aliases.append(itemlst[i])
                   
                hosts.append({'ip':ip.group(), 'name':itemlst[1], 'target':hostfile, 'host_aliases':aliases})

        except IOError:
            return hosts

        return hosts
