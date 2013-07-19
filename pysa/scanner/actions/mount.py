'''
Scans mount points

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

import logging
import os

from pysa.scanner.actions.base import ScannerBase


class ScannerMount(ScannerBase):
    
    def scan(self):
        self.__disk_usage()
    
    def __disk_partitions(self,all=False):  
        """
        Return all mountd partitions as a dict.    
        """  
        phydevs = []  
        f = open("/proc/filesystems", "r")  
        for line in f:  
            if not line.startswith("nodev"):  
                phydevs.append(line.strip())  
      
        retlist = {} 
        f = open('/etc/mtab', "r")  
        for line in f:  
            if not all and line.startswith('none'):
                continue
            fields                 = line.split()  
            device                 = fields[0]  
            mountpoint             = fields[1]  
            fstype                 = fields[2]  
            if not all and fstype not in phydevs:  
                continue  
            if device == 'none':  
                device             = ''
            retlist[device]        = (device, mountpoint, fstype)
        return retlist  
    
    def __disk_usage(self):  
        """Return disk usage associated with path."""  
        disk                     = self.__disk_partitions()
        for device in disk.keys():
            st = os.statvfs(device)
            size = st.f_blocks * st.f_frsize
            self.add_mount(device=device, fstype=disk[device][2], name=disk[device][1], size=size)
