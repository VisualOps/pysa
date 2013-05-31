'''
Created on 2013-04-09

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

import os
import logging
import subprocess
from collections import defaultdict

from base import scanner_base
import utils

class scanner_source(scanner_base):

    def scan(self):
        """
        scan repository
        """
        logging.info('searching for repository')

        self.user_repos = {'git':[], 'svn':[], 'hg':[]}    # save all the scm repos

        self.search_scm('/')
        #self.search_scm('svn', '/')
        #self.search_scm('hg', '/')
        self.add_repos()

    def search_scm(self, dir):
        """
        search all scm repositories in local directory dirname
        """
        """
        try:
            if scm=='git':
                scm_flag = '.git'
            elif scm=='svn':
                scm_flag = '.svn'
            elif scm=='hg':
                scm_flag = '.hg'

            p = subprocess.Popen(['-c', 'find '+dirname+' -type d -name ' + scm_flag + ' 2>/dev/null |  xargs -n 1 dirname'],
                shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except OSError:
            return

        for dir in p.stdout:
            dir = dir.strip()
            if scm=='svn':  #if svn scm, need to check subdirctory
                head, tail = os.path.split(dir)
                while head and tail:
                    if head in self.user_repos['svn']:
                        break
                    head, tail = os.path.split(head)
                else:
                    subsvn = [ scmdir for scmdir in self.user_repos['svn'] if dir in scmdir ]
                    if len(subsvn)>0:
                        for subdir in subsvn: self.user_repos['svn'].remove(subdir)

                    self.add_local_repo(scm, dir)
            else:
                self.add_local_repo(scm, dir)
        """

        for dirpath, dirnames, filenames in os.walk(dir):
            for dirname in dirnames:
                if dirname == '.git':
                    scm = 'git'
                elif dirname == '.svn':
                    scm = 'svn'
                elif dirname == '.hg':
                    scm = 'hg'
                else:
                    continue

                if scm=='svn':  #if svn scm, need to check subdirctory
                    head, tail = os.path.split(dirpath)
                    while head and tail:
                        if head in self.user_repos['svn']:
                            break
                        head, tail = os.path.split(head)
                    else:
                        subsvn = [ scmdir for scmdir in self.user_repos['svn'] if dirpath in scmdir ]
                        if len(subsvn)>0:
                            for subdir in subsvn: self.user_repos['svn'].remove(subdir)

                        self.add_local_repo(scm, dirpath)
                else:
                    self.add_local_repo(scm, dirpath)

    def add_repos(self):
        """
        get the repository info and add repo
        """
        for (scm, dirs) in self.user_repos.items():
            for dirname in dirs:
                sources = []    # http/ssh
                branches = []

                try:
                    if scm=='git':
                        p = subprocess.Popen(['-c', 'git --git-dir=' + dirname + '/.git --work-tree=' + dirname+' remote -v'],
                            stdout=subprocess.PIPE, shell=True)
                        for line in p.stdout:
                            src = line.split('\t')[1].split(' ')[0]
                            if src is not None and src not in sources:
                                sources.append(src)

                        # branches
                        p = subprocess.Popen(['-c', 'git --git-dir=' + dirname + '/.git --work-tree=' + dirname + ' branch'],
                            stdout=subprocess.PIPE, shell=True)
                        for line in p.stdout:
                            if line is not None:
                                lst = line.strip().split()
                                for br in lst:
                                    if br is not None and br!='*':
                                        branches.append(br)

                    elif scm=='svn':
                        p = subprocess.Popen(['-c', 'svn info ' + dirname + ' | grep URL | awk \'{print $NF}\''],
                            shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

                        for source in p.stdout:
                            if source is not None: sources.append(source.strip())

                        ### branches
                    elif scm=='hg':
                        # sources
                        p = subprocess.Popen(['-c', 'hg paths -R' + dirname], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                        for line in p.stdout:
                            source = line.split('=')[1].strip()
                            if source is not None and source not in sources: sources.append(source)
                        # branches
                        p = subprocess.Popen(['-c', 'hg branches -R' + dirname], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                        for line in p.stdout:
                            branch = line.strip().split(' ')[0]
                            if branch is not None and branch not in branches: branches.append(branch)
                    else:
                        continue

                except OSError:
                    continue

                # add the public info
                s = utils.get_stat(dirname)

                if len(sources)<=0: continue

                self.add_source(sources[0], os.path.basename(dirname), dirname, s[2], s[0], s[1], scm, branches)

    @property
    def user_repos(self):
        """
        local repos
        """
        if user_repos not in self:
            self.user_repos = defaultdict(list)

        return self.user_repos

    def add_local_repo(self, scm, dirname):
        """
        add all repos to local repos
        """
        if scm not in self.user_repos:
            self.user_repos[scm] = []

        self.user_repos[scm].append(dirname)
