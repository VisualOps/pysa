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

from pysa.config import *
from pysa.scanner.actions.base import ScannerBase


class ScannerService(ScannerBase):
    # Patterns for determining which Upstart services should be included, based
    # on the events used to start them.
    UPSTART_PATTERN1 = re.compile(r'start\s+on\s+runlevel\s+\[[2345]', re.S)
    UPSTART_PATTERN2 = re.compile(r'start\s+on\s+\([^)]*(?:filesystem|filesystems|local-filesystems|mounted|net-device-up|remote-filesystems|startup|virtual-filesystems)[^)]*\)', re.S)
    
    def scan(self):
        """
        scan service:
        search the service config files
        """
        logging.info('searching for system services')

        for dir in ['/etc/init', 
                    '/etc/init.d',
                    '/etc/rc.d/init.d']:
            for dirname, dirnames, filenames in os.walk(dir):
                for filename in filenames:
                    try:
                        pathname = os.path.join(dirname, filename)
                        dict = self.parse_service(pathname)

                        # add service
                        if dict != None:
                            # format (provider, name, enable, hasrestart)
                            self.add_service(enable=dict['enable'], hasrestart=dict['hasrestart'], 
                                name=dict['name'], path=dirname, provider=dict['provider'], hasstatus=dict['hasstatus'])
                    except ValueError:
                        pass
            
    def parse_service(self, pathname):
        """
        Parse a potential service init script or config file into the
        manager and service name or raise `ValueError`.  Use the Upstart
        "start on" stanzas and SysV init's LSB headers to restrict services to
        only those that start at boot and run all the time.
        
        ###Need to add systemd service parse.
        """
        
        dirname, basename = os.path.split(pathname)
        if '/etc/init' == dirname:
            service, ext = os.path.splitext(basename)
            
            # Ignore extraneous files in /etc/init.
            if '.conf' != ext:
                raise ValueError('not an Upstart config')

            # Ignore services that don't operate on the (faked) main runlevels.
            try:
                content = open(pathname).read()
            except IOError:
                raise ValueError('not a readable Upstart config')
                
            enable = False    
            if (self.UPSTART_PATTERN1.search(content) \
                    or self.UPSTART_PATTERN2.search(content)):
                enable = True

            return {'provider':'upstart', 'name':service, 'enable':enable, 
                'hasrestart':False, 'hasstatus':False}
                
        elif '/etc/init.d' == dirname or '/etc/rc.d/init.d' == dirname:
            #import pdb
            #pdb.set_trace()

            # Let Upstart handle its services.
            if os.path.islink(pathname) \
                and '/lib/init/upstart-job' == os.readlink(pathname):
                raise ValueError('proxy for an Upstart config')

            # Ignore services that don't operate on the main runlevels.
            try:
                content = open(pathname).read()
            except IOError:
                raise ValueError('not a readable SysV init script')
                
            enable = False    
            if re.search(r'(?:Default-Start|chkconfig):\s*[-2345]', content):
                enable = True
            
            hasrestart = False
            if re.search(r'\s*(?:restart|reload)\)\s*', content):
                hasrestart = True
            
            hasstatus = False
            if re.search(r'\s*status\)\s*', content):
                hasstatus = True
            
            return {'provider':'init', 'name':basename, 'enable':enable,
                'hasrestart':hasrestart, 'hasstatus':hasstatus}       ### change sysvinit to init
        else:
            raise ValueError('not a service')
