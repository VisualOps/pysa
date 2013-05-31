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

import re
import os
import stat
import pwd
import grp
import subprocess
import logging
import string

PAT_IP = re.compile(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', re.S)
TEXT_CHARACTERS = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
NULL_TRANS = string.maketrans("", "")

def lsb_release_codename():
    """
    Return the OS release's codename.
    """
    if hasattr(lsb_release_codename, '_cache'):
        return lsb_release_codename._cache
    try:
        p = subprocess.Popen(['lsb_release', '-c'], stdout=subprocess.PIPE)
    except OSError:
        lsb_release_codename._cache = None
        return lsb_release_codename._cache
    stdout, stderr = p.communicate()
    if 0 != p.returncode:
        lsb_release_codename._cache = None
        return lsb_release_codename._cache
    match = re.search(r'\t(\w+)$', stdout)
    if match is None:
        lsb_release_codename._cache = None
        return lsb_release_codename._cache
    lsb_release_codename._cache = match.group(1)
    return lsb_release_codename._cache

def rubygems_unversioned():
    """
    Determine whether RubyGems is suffixed by the Ruby language version.
    It ceased to be on Oneiric.  It always has been on RPM-based distros.
    """
    codename = lsb_release_codename()
    return codename is None or codename[0] >= 'o'

def rubygems_virtual():
    """
    Determine whether RubyGems is baked into the Ruby 1.9 distribution.
    It is on Maverick and newer systems.
    """
    codename = lsb_release_codename()
    return codename is not None and codename[0] >= 'm'

def rubygems_path():
    """
    Determine based on the OS release where RubyGems will install gems.
    """
    if lsb_release_codename() is None or rubygems_update():
        return '/usr/lib/ruby/gems'
    return '/var/lib/gems'

def mtime(pathname):
    try:
        return os.stat(pathname).st_mtime
    except OSError:
        return 0

# open the cache file
def open_cache(pathname, mode):
    f = open(pathname, mode)
    uid = int(os.environ['SUDO_UID'])
    gid = int(os.environ['SUDO_GID'])
    os.fchown(f.fileno(), uid, gid)
    return f

def valid_txtfile(pathname):
    # only file
    if os.path.isdir(pathname)==True:
        return False
        
    # only plane text file
    ###########################################
    #cmd = '/usr/bin/file -bi ' + pathname
    #f = os.popen(cmd, 'r')
    #if f.read().startswith('text') == False:
    #    return False
    ###########################################
    if istextfile(pathname)==0:
        return False

    # get the ctime;
    s = os.lstat(pathname)
    # And ignore block special files, character special files,
    # pipes, sockets and symbolic links.
    if stat.S_ISBLK(s.st_mode) \
    or stat.S_ISCHR(s.st_mode) \
    or stat.S_ISFIFO(s.st_mode) \
    or stat.S_ISSOCK(s.st_mode) \
    or stat.S_ISLNK(s.st_mode):
        return False

    return True

def istextfile(filename, blocksize = 512):
   try:
        ret = istext(open(filename).read(blocksize))
   except IOError:
        return 0
   return ret

def istext(s):
    if "\0" in s:
        return 0

    if not s:  # Empty files are considered text
        return 1

    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(NULL_TRANS, TEXT_CHARACTERS)

    # If more than 30% non-text characters, then
    # this is considered a binary file
    if len(t)/len(s) > 0.30:
        return 0
    return 1

def get_stat(pathname):
    try:
        s = os.lstat(pathname)
        pw = pwd.getpwuid(s.st_uid)
        owner = pw.pw_name

        gr = grp.getgrgid(s.st_gid)
        group = gr.gr_name

        mode = oct( s.st_mode & 0777 )

    except KeyError:
        owner = s.st_uid
        group = s.st_gid
        mode = oct( 0777 )

    return (group, mode, owner)

def get_content(pathname):
    # read the config file's content
    try:
        content = open(pathname).read()
        return content
    except IOError, e:
        logging.error('utils.get_content(): Can not get file content, %s' % str(e))
        return  None

def get_ips(filename):
    ips = []
    try:
        file = open(filename, "r")

        # read through the file
        for line in file.readlines():
            line = line.rstrip()

            regex = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
            # if the regex is not empty and is not already in ips list append
            for ip in regex:
                if ip is not None and ip not in ips:
                    if (PAT_IP.match(ip)) and (not ip.startswith('127.')) and (not ip.startswith('0.')):
                        ips.append(ip)

        file.close()

    except IOError, (errno, strerror):
        return ips

    return ips
