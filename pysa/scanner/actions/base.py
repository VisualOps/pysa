'''
Created on 2013-3-27

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

import subprocess
import logging
import re

from pysa.exception import *
from pysa.scanner.object.package import package
from pysa.scanner.object.file import file
from pysa.scanner.object.user import user
from pysa.scanner.object.service import service
from pysa.scanner.object.repository import repository
from pysa.scanner.object.group import group
from pysa.scanner.object.cron import cron
from pysa.scanner.object.host import host
from pysa.scanner.object.mount import mount
from pysa.scanner.object.sshkey import sshkey
from pysa.scanner.object.source import source
from pysa.scanner.object.process import process


class scanner_base():
    def __init__(self, packages, files, crons, groups, mounts, hosts, repos, services, sshkeys, users, ips, sources, proces):
        self.packages = packages
        self.files = files
        self.crons = crons
        self.groups = groups
        self.mounts = mounts
        self.hosts = hosts
        self.repos = repos
        self.services = services
        self.keys = sshkeys
        self.users = users
        self.ips = ips
        self.sources = sources
        self.proces = proces

    def scan(self):
        '''
        Implement in ScannerYum, ScannerApt...
        '''
        pass

    @GeneralException
    def subprocess(self, command):
        logging.info('ScannerBase.subprocess(): Command, %s' % str(command))
        try:
            # redirect the err to /dev/null
            devnull = open('/dev/null', 'w')
            p = subprocess.Popen(
                                 command,
                                 close_fds=True,
                                 stdout=subprocess.PIPE,
                                 stderr=devnull
                                 )
            return self.__generator(p.stdout)
        except OSError:
            logging.debug("ScannerBase.subprocess(): commnand failed, command: %s" % str(command))
            return

    @GeneralException
    def __generator(self, stdout):
        for line in stdout:
            yield line

    @GeneralException
    def add_package(self, *args, **kargs):
        _package = package(*args, **kargs)

        if self.rules:
            # attribute filter
            if _package.attr_filter(self.rules['discard']): return
            # additional filter
            _package.add_filter(self.rules['addition'])

        self.packages[_package.primaryvalue] = _package.prase()

    @GeneralException
    def get_packages(self):
        return self.packages

    @GeneralException
    def add_file(self, *args, **kargs):
        _file = file(*args, **kargs)

        if self.rules:
            if _file.attr_filter(self.rules['discard']): return
            _file.add_filter(self.rules['addition'])

        self.files[_file.primaryvalue] = _file.prase()

    @GeneralException
    def get_files(self):
        return self.files

    @GeneralException
    def add_user(self, *args, **kargs):
        _user = user(*args, **kargs)

        if self.rules:
            if _user.attr_filter(self.rules['discard']): return
            _user.add_filter(self.rules['addition'])

        self.users[_user.primaryvalue] = _user.prase()

    @GeneralException
    def get_users(self):
        return self.users

    @GeneralException
    def add_service(self, *args, **kargs):
        _service = service(*args, **kargs)

        if self.rules:
            if _service.attr_filter(self.rules['discard']): return
            _service.add_filter(self.rules['addition'])

        self.services[_service.primaryvalue] = _service.prase()

    @GeneralException
    def get_services(self):
        return self.services

    @GeneralException
    def add_repo(self, *args, **kargs):
        _repo = repository(*args, **kargs)  

        if self.rules:     
            if _repo.attr_filter(self.rules['discard']): return
            _repo.add_filter(self.rules['addition'])

        self.repos[_repo.primaryvalue] = _repo.prase()

    @GeneralException
    def get_repos(self):
        return self.repos

    @GeneralException
    def add_group(self, *args, **kargs):
        _group = group(*args, **kargs)

        if self.rules:
            if _group.attr_filter(self.rules['discard']): return
            _group.add_filter(self.rules['addition'])

        self.groups[_group.primaryvalue] = _group.prase()

    @GeneralException
    def get_groups(self):
        return self.groups

    @GeneralException
    def add_cron(self, *args, **kargs):
        _cron = cron(*args, **kargs)

        if self.rules:
            if _cron.attr_filter(self.rules['discard']): return
            _cron.add_filter(self.rules['addition'])

        self.crons[_cron.primaryvalue] = _cron.prase()

    @GeneralException
    def get_crons(self):
        return self.crons

    @GeneralException
    def add_host(self, *args, **kargs):
        _host = host(*args, **kargs)

        if self.rules:
            if _host.attr_filter(self.rules['discard']): return
            _host.add_filter(self.rules['addition'])

        self.hosts[_host.primaryvalue] = _host.prase()

    @GeneralException
    def get_hosts(self):
        return self.hosts

    @GeneralException
    def add_mount(self, *args, **kargs):
        _mount = mount(*args, **kargs)

        if self.rules:
            if _mount.attr_filter(self.rules['discard']): return
            _mount.add_filter(self.rules['addition'])

        self.mounts[_mount.primaryvalue] = _mount.prase()

    @GeneralException
    def get_mounts(self):
        return self.mounts

    @GeneralException
    def add_key(self, *args, **kargs):
        _key = sshkey(*args, **kargs)

        if self.rules:
            if _key.attr_filter(self.rules['discard']): return
            _key.add_filter(self.rules['addition'])
            
        self.keys[_key.primaryvalue] = _key.prase()

    @GeneralException
    def get_keys(self):
        return self.keys

    @GeneralException
    def add_ip(self, mip):
        self.ips.append(mip)

    @GeneralException
    def get_ips(self):
        return self.ips

    @GeneralException
    def add_source(self, *args, **kargs):
        _source = source(*args, **kargs)

        if self.rules:
            if _source.attr_filter(self.rules['discard']): return
            _source.add_filter(self.rules['addition'])

        self.sources[_source.primaryvalue] = _source.prase()

    @GeneralException
    def get_sources(self):
        return self.sources

    @GeneralException
    def add_proc(self, *args, **kargs):
        _process = process(*args, **kargs)

        if self.rules:
            if _process.attr_filter(self.rules['discard']): return
            _process.add_filter(self.rules['addition'])

        self.proces[_process.primaryvalue] = _process.prase()

    @GeneralException
    def get_proces(self):
        return self.proces

    @GeneralException
    def init_filter(self, rules=None):
        """
        init the filter rules
        """
        
        self.rules = rules

        if self.rules:  # init the discard and addition rules if not
            if 'discard' not in self.rules: self.rules['discard'] = {}
            if 'addition' not in self.rules: self.rules['addition'] = {}
