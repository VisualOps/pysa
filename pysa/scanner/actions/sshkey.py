'''
Get SSH keys

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
import re

from pysa.config import config
from pysa.scanner.actions.base import scanner_base
from pysa.scanner.actions.utils import *


class scanner_key(scanner_base):
    
    support_key_type = [
                        'ssh-rsa',
                        'ssh-dss',
                        'ecdsa-sha2-nistp256',
                        'ecdsa-sha2-nistp384',
                        'ecdsa-sha2-nistp521'
                        ]
    
    scan_file_type = [
                      '.pub',
                      '.pem'
                      ]
    
    re_pattern = "-----.+-----"
    
    path_dir = config.key_path
    
    def scan(self):
        for dirpath, dirnames, filenames in os.walk(self.path_dir):
            for filename in filenames:
                try:
                    # key with specific name
                    if '.' in filename:
                        for file_type in self.scan_file_type:
                            if filename.endswith(file_type):
                                full_path = os.path.join(dirpath, filename)
                                mode = get_stat(full_path)[1]
                                content = get_content(full_path)
                                if content:
                                    _type = self.__get_type(content)
                                    self.add_key(key=content, name=filename, _type=_type, path=full_path, mode=mode)
                                    logging.debug('ScannerKey.scan(): Add key file %s' % filename)
                        
                    # key without specific name
                    else:
                        full_path = os.path.join(dirpath, filename)
                        mode = get_stat(full_path)[1]
                        content = get_content(full_path)
                        if content and re.match(self.re_pattern, content):
                            _type = self.__get_type(content)
                            self.add_key(key=content, name=filename, _type=_type, path=full_path, mode=mode)
                            logging.debug('ScannerKey.scan(): Add key file %s' % filename)
                            
                except Exception, e:
                    #log
                    logging.error("ScannerKey.scan(): Add file %s failed, %s" % (filename, str(e)))
                    
                
    def __get_type(self, content):
        for _type in self.support_key_type:
            if _type in content:
                return _type
