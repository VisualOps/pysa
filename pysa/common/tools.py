'''
Common tools

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

@author: Thibault BRONCHAIN
'''

import os
import os.path
import logging
import re

from common.exception import *


INFO    = "INFO"
DEBUG   = "DEBUG"
ERR     = "ERROR"

LOGGING_EQ = {
    INFO        : logging.info,
    DEBUG       : logging.debug,
    ERR         : logging.error
}


# common tools collection
class tools():
    # logging
    @staticmethod
    def l(action, content, f, c = None):
        out = ""
        if c:
            out += "%s." % (c.__class__.__name__)
        out += "%s()" % (f)
        LOGGING_EQ[action]("%s: %s" % (out, content))

    # add a tab
    @staticmethod
    def tab_inc(tab):
        return tab+'\t'

    # delete a tab
    @staticmethod
    def tab_dec(tab):
        return tab[1:]

    # write data in a specific file
    @staticmethod
    def write_in_file(fname, content):
        tools.l(INFO, "creating file %s" % (fname), 'write_in_file')
        dirname = os.path.dirname(fname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        f = open(fname,'w')
        f.write(content)
        f.close()

    # get recursive path dirlist
    @staticmethod
    def get_recurse_path(path):
        rpath = re.split('/', path)
        i = 1
        while i < len(rpath):
            rpath[i] = os.path.normpath("%s/%s" % (rpath[i-1] if i else "", rpath[i]))
            i += 1
        rpath[0] = '/'
        return rpath

    # get previous path
    @staticmethod
    def path_basename(path):
        if path == '/': return None
        if path[-1] == '/': path = path[:-1]
        rpath = re.split('/', path)
        i = 1
        while i < len(rpath):
            rpath[i] = os.path.normpath("%s/%s" % (rpath[i-1] if i else "", rpath[i]))
            i += 1
        rpath[0] = '/'
        if len(rpath) < 2: return None
        return rpath[-2]

    # returns file content
    @staticmethod
    def get_file(filename):
        if not filename: return None
        file = None
        try:
            f = open(filename, 'r')
            file = f.read()
        except IOError:
            tools.l(ERR, "%s: no such file or directory" % (filename), 'dump_file')
            return None
        return file

    # check if file exists
    @staticmethod
    def file_exists(filename):
        if not filename: return None
        try:
            with open(filename): pass
        except IOError:
            tools.l(ERR, "%s: no such file or directory" % (filename), 'file_exists')
            return None
        return filename

    # merge lists recursive
    @staticmethod
    def list_merging(first, second):
        f = (first if first else [])
        s = (second if second else [])
        return f+s

    # remove childs after dict merging
    @staticmethod
    def dict_cleaner(input):
        output = {}
        for key in input:
            if type(input[key]) is not dict:
                output[key] = input[key]
        return output

    # ensure dictionary existency
    @staticmethod
    def s_dict_merging(first, second):
        d = tools.dict_merging(first,second)
        return (d if d else {})

    # merge dicts /!\ recursive
    @staticmethod
    def dict_merging(first, second):
        if (not first) and (not second):
            return None
        elif not first:
            return dict(second.items())
        elif not second:
            return dict(first.items())
        repl = dict(first.items())
        for item in second:
            if (first.get(item)) and (type(first[item]) != type (second[item])):
                continue
            elif not first.get(item):
                repl[item] = second[item]
            elif type(second[item]) is dict:
                # recursion here
                val = tools.dict_merging(first[item], second.get(item))
                if val != None:
                    repl[item] = val
            elif type(second[item]) is list:
                repl[item] = first[item] + second[item]
            else:
                repl[item] = second[item]
        return repl
