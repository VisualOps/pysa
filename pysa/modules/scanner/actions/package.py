'''
Created on 2013-04-10

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
import os.path
import logging
import subprocess

from base import scanner_base
import utils

# define the scan modes
scan_modes = ['yum', 'rpm', 'sub_rpm', 'apt', 'sub_dpkg']

class scanner_package(scanner_base):
    def scan(self):
        """
        scan package
        first search with yum, next with apt and with subprocess at last
        """
        logging.info('searching for packages')

        self.core_pkgs = {}
        self.user_pkgs = {}
        self.ip_list = []

        if self.scan_yum()==False:
           if self.scan_rpm()==False:
                if self.scan_apt()==False:
                    self.scan_subprocess()

        # add the user package list
        self.add_pkgs()

        # add ips
        for ip in self.ip_list:
            self.add_ip(ip)

    def scan_yum(self):
        """
        scan the redhat family platform with yum api
        """
        try:
            import yum
        except ImportError:
            return False

        logging.info('searching for yum packages')

        self.scan_mode = 'yum'

        yb = yum.YumBase()
        # get all installed packages and check each's dependency
        yb.conf.cache = 1
        for pkg in sorted(yb.rpmdb.returnPackages()):
            pkgtag = pkg.__str__()

            # skip the package which is in the core package list
            if pkgtag in self.core_pkgs:
                continue

            reqs = pkg.required_packages()
            # remove packages which is in the requiring list from user packages
            # and add packages which is not in core packages from dependency list
            for req in reqs:
                reqtag = req.__str__()
                if reqtag in self.user_pkgs:
                    del self.user_pkgs[reqtag]

                if reqtag not in self.core_pkgs:
                    self.core_pkgs[reqtag] = req

            thepkg = yb.pkgSack.searchNevra(pkg.name, pkg.epoch, pkg.version, pkg.release, pkg.arch)  #epoch=None, ver=None, rel=None, arch=None
            if len(thepkg)==0 or thepkg[0].verEQ(pkg)==False:
                continue

            self.user_pkgs[pkgtag] = pkg

        return True

    def scan_rpm(self):
        """
        scan the redhat family platform with rpm api
        """
        try:
            import rpm
        except ImportError:
            return False

        logging.info('searching for rpm packages')

        self.scan_mode = 'rpm'

        ts = rpm.TransactionSet()
        mi = ts.dbMatch()
        for h in mi:
            if h[rpm.RPMTAG_EPOCH]==None:
                epoch = '(none)'
            pkgtag = '%s-%s-%s.%s-%s' % (h[rpm.RPMTAG_NAME], h[rpm.RPMTAG_VERSION],
                h[rpm.RPMTAG_RELEASE], h[rpm.RPMTAG_ARCH], epoch)

            # skip the package in the core package list already
            if pkgtag in self.core_pkgs:
                continue

            # query the package dependency
            for req in h[rpm.RPMTAG_REQUIRENAME]:
                if req.find(' ')>=0:
                    req = req[0:req.find(' ')]
                if req.startswith('rpmlib'):    continue

                try:
                    p = subprocess.Popen(['rpm',
                                      '-q',
                                      '--qf=%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}-%{EPOCH}',
                                      '--whatprovides',
                                      req],
                                     close_fds=True,
                                     stdout=subprocess.PIPE)
                    reqtag, stderr = p.communicate()
                    # ignore the package itself
                    if reqtag==pkgtag: continue
                except OSError: continue

                if reqtag in self.user_pkgs:
                    del self.user_pkgs[reqtag]
                if reqtag not in self.core_pkgs:
                    self.core_pkgs[reqtag] = req   ### need to query the req_pkg's header

                self.user_pkgs[pkgtag] = h

        return True

    def scan_apt(self):
        """
        searching at the debian family platform with apt package
        http://apt.alioth.debian.org/python-apt-doc/
        """
        try:
            import apt
        except ImportError:
            return False

        logging.info('searching for Apt packages')

        self.scan_mode = 'apt'

        apt_cache = apt.Cache()
#        apt_cache.update()
#        apt_cache.open()

        DEP_TYPES = ['Depends', 'Recommends', 'Suggests', 'Replaces', 'Enhances']

        for package_name in apt_cache.keys():
            pkg = apt_cache[package_name]

            #Verify that the package is installed
            if hasattr(pkg, 'isInstalled'):
                if not pkg.isInstalled:    continue
            elif hasattr(pkg, 'is_installed'):
                if not pkg.is_installed:    continue
            else:
                continue


            pkgid = pkg.id

            for pkgv in pkg.versions:
                deps = self.ext_aptdeps(pkgv, 'Depends')

                for dep in deps:
                    # check the dep_pkg's name
                    if dep.name not in apt_cache: continue
                    # query the dep_pkg
                    dep_pkg = apt_cache[dep.name]

                    depid = dep_pkg.id

                    if hasattr(pkg, 'isInstalled'):
                        if not pkg.isInstalled:    continue
                    elif hasattr(pkg, 'is_installed'):
                        if not pkg.is_installed:    continue
                    else:
                        continue

                    if depid in self.user_pkgs:
                        del self.user_pkgs[depid]

                    if depid not in self.core_pkgs:
                        self.core_pkgs[depid] = dep_pkg

            self.user_pkgs[pkgid] = pkg

        return True

    def ext_aptdeps(self, pkg, dep_type):
        """
        generate the package's dependencies of particular dependency type
        """
        for dep_pkglst in pkg.get_dependencies(dep_type):
            for dep_pkg in dep_pkglst.or_dependencies:
                yield dep_pkg

    def scan_subprocess(self):
        """
        searching package with subprocess
        """
        logging.info('searching with subprocess')

        self.scan_mode = 'sub_rpm'
        lines = self.subprocess(['rpm', '--qf=%{NAME}\x1E%{VERSION}\x1E%{RELEASE}\x1E%{ARCH}\x1E%{EPOCH}\x1E%{SUMMARY}\x1E%{VENDOR}\n', '-qa'])
        if lines==None:
            # try apt of the Debian family system
            self.scan_mode = 'sub_dpkg'

            lines = self.subprocess(['dpkg-query', '-W',
                '-f=${Status}\x1E${Package}\x1E${Version}\x1E${Architecture}\n'])

            if lines==None:
                logging.info('searching packages failed')
                return

        # parse the stdout [michael, 2013/03/28]
        for line in lines:
            if self.scan_mode=='sub_rpm':
                pkg, ver, rel, arch, epo, sum, ven = line.strip().split('\x1E')
                pkg_tag = pkg + '-' + ver + '-' + rel + '.' + arch + '-' +  epo
            elif self.scan_mode=='sub_dpkg':
                status, pkg, ver, arch = line.strip().split('\x1E')
                if 'install ok installed' != status: continue
                pkg_tag = pkg + '-' + ver + '-' + arch
            else:
                return

            if pkg_tag in self.core_pkgs:   continue

            # query the dependency
            self.query_deps(pkg)

            confs = []
            if self.scan_mode=='sub_rpm':
                # query config files
                conffiles = self.subprocess(['rpm', '-qc', pkg])
                for fi in conffiles:
                    file = fi.strip()
                    confs.append(file)

                self.user_pkgs[pkg_tag] = {
                    'name':pkg, 'version':ver, 'release':rel, 'arch':arch, 'epoch':epo, 'summary':sum, 'vendor':ven, 'configs':confs}

            if self.scan_mode=='sub_dpkg':
                conffiles = self.subprocess(['dpkg-query', '-W', '-f=${Conffiles}', pkg])
                for fi in conffiles:
                    file = fi.strip().split(' ')[0]
                    confs.append(file)

                self.user_pkgs[pkg_tag] = {'name':pkg, 'version':ver, 'arch':arch, 'configs':confs}

    def add_conffile(self, filepath):
        """
        check and add the package's config file
        """
        ### config file(in 'etc' directory)
        if filepath.startswith(('/etc/', '/home/'))==False:
            return False
        ### suffix list[conf, cfg, ini]
        filename, suffix = os.path.splitext(filepath)
        if suffix not in ['.conf', '.cfg', '.ini']:
            return False

        # get the config file's information and add it
        # only plane text file
        if utils.valid_txtfile(filepath) == False:
            return False

        # get owner, group and mode
        s = utils.get_stat(filepath)

        # read the config file's content
        c = utils.get_content(filepath)

        # add the config file:
        # checksum, content, group, mode, owner, path, force=False, provider=None,
        # recurse=None, recurselimit=None, source=None
        self.add_file('md5', c, s[0], s[1], s[2], filepath)

        return True

    def query_deps(self, package):
        """
        query package's denpendency in the list and update the user/core package list
        """

        if self.scan_mode == 'sub_rpm':
            reqs = self.subprocess(['rpm', '-qR', package])

            for req in reqs:
                req = req.strip()
                # query the dependency package
                infos = self.subprocess(['rpm', '-q',
                    '--qf=%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}-%{EPOCH}\n',
                    '--whatprovides', req])

                for info in infos:
                    dep_tag = info.strip().split('\x1E')[0]

                    # check dependency package whether in the user package list
                    if dep_tag in self.user_pkgs:   del self.user_pkgs[dep_tag]

                    # check dependency package whether in the core package list
                    if dep_tag not in self.core_pkgs: self.core_pkgs[dep_tag] = dep_tag

        elif self.scan_mode == 'sub_dpkg':
            # query the dependency
            deplines = self.subprocess(['dpkg-query', '-W', '-f=${Depends}\n', package])

            for line in deplines:
                deps = re.split(', |\|', line.strip())

                for dep in deps:
                    if dep.find(' '):
                        dep = dep[0:dep.find(' ')]

                    infos = self.subprocess(['dpkg-query', '-W',
                        '-f=${Status}\x1E${Package}-${Version}-${Architecture}\n', dep])
                    for line in infos:
                        status, dep_tag = line.strip().split('\x1E')

                        if 'install ok installed' != status:    continue

                        if dep_tag in self.user_pkgs:
                            del self.user_pkgs[dep_tag]

                        if dep_tag not in self.core_pkgs:
                            self.core_pkgs[dep_tag] = dep_tag

        else:
            return

    @property
    def user_pkgs(self):
        return self.user_pkgs

    @property
    def core_pkgs(self):
        return self.core_pkgs

    @property
    def ip_list(self):
        return self.ip_list

    def add_user_pkg(self, pkg_tag, pkg):
        self.user_pkgs[pkg_tag] = pkg

    def add_core_pkg(self, pkg_tag, pkg):
        self.core_pkgs[pkg_tag] = pkg

    def add_ips(self, ex_ips):
        self.ip_list = list(set(self.ip_list+ex_ips))

    @property
    def scan_mode(self):
        return self.scan_mode

    def set_scan_mode(self, mode):
        if mode not in scan_modes:
            self.scan_mode = 'yum'
        else:
            self.scan_mode = mode

    def add_pkgs(self):
        """
        add packages
        """
        if self.scan_mode=='yum' or self.scan_mode=='rpm':
            try:
                import rpm
            except ImportError:
                return

            ts = rpm.TransactionSet()
            for (pkg_tag, pkg) in self.user_pkgs.items():
                if self.scan_mode == 'yum':
                    name = pkg.name
                if self.scan_mode == 'rpm':
                    name = pkg[rpm.RPMTAG_NAME]

                ### search the yum api of searching package's config files
                mi = ts.dbMatch('name', name)
                for h in mi:
                    # save the config files
                    confs = []

                    fi = h.fiFromHeader()
                    for file in fi:
                        fipath = file[0]

                        if fipath in confs:
                            continue

                        if self.add_conffile(fipath)==False:
                            continue

                        tmpips = utils.get_ips(fipath)
                        self.add_ips(tmpips)

                        confs.append(fipath)

                    # get the epoch
                    #epoch = h['epoch'] if h['epoch'] else 0

                    # add package
                    self.add_package(name, manager='yum', provider='yum', files=confs,
                                description=h['summary'], platform=h['arch'],
                                version=h['version']+'-'+h['release'], vendor=h['vendor'])

        elif self.scan_mode=='apt':
            for (id, pkg) in self.user_pkgs.items():

                # pkg's config files
                confs = []
                fi = pkg.installed_files
                for file in fi:
                    if file in confs: continue

                    if self.add_conffile(file)==False: continue

                    tmpips = utils.get_ips(file)
                    self.add_ips(tmpips)

                    confs.append(file)

                for pkgv in pkg.versions:
                    self.add_package(pkg.shortname, manager='apt', provider='apt', files=confs,
                        description=pkgv.summary, platform=pkgv.architecture, version=pkgv.version)

        elif self.scan_mode=='sub_rpm':
            for (tag, info) in self.user_pkgs.items():
                #'name':name, 'version':ver, 'release':rel, 'arch':arch, 'epoch':epo, 'summary':sum, 'vendor':ven, 'configs':confs

                confs = []
                # parse the ips
                for file in info['configs']:
                    if file in confs: continue

                    if self.add_conffile(file)==False: continue

                    tmpips = utils.get_ips(file)
                    self.add_ips(tmpips)

                    confs.append(file)

                #epoch = info['epoch'] if info['epoch'] else 0
                # add the package
                self.add_package(info['name'], manager='rpm', provider='rpm', files=confs,
                                 description=info['summary'], platform=info['arch'], version=info['version']+'-'+info['release'])

        elif self.scan_mode=='sub_dpkg':
            for (tag, info) in self.user_pkgs.items():
                confs = []
                for file in info['configs']:
                    #{'name':name, 'version':ver, 'arch':arch, 'description':desc, 'configs':conffiles}
                    if file in confs: continue

                    if self.add_conffile(file)==False: continue

                    tmpips = utils.get_ips(file)
                    self.add_ips(tmpips)

                    confs.append(file)

                self.add_package(info['name'], manager='dpkg', provider='dpkg',
                                 files=confs, version=info['version'])

