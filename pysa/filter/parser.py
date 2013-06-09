'''
Apply user filters

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

from ConfigParser import SafeConfigParser

from pysa.tools import *
from pysa.exception import *


class ParserException(Exception): pass

filters_split = ['discard', 'addition']
filters_req = {
    'replace': {
        '_replaceall': [True, False]
        },
    'update': {
        '_update': [True, False]
        }
}

global_filters = {
    'discard': {
        'file' : {
            'path' : [
                '/etc/fstab',
                '/etc/group',
                '/etc/gshadow-',
                '/etc/hosts',
                '/etc/passwd',
                '/etc/passwd-',
                '/etc/shadow',
                '/etc/shadow-',
                ]
            }
        }
}


# filters parser
class fparser():
    def __init__(self, filename):
        self.__filename = tools.file_exists(filename)

    # action
    @general_exception
    def run(self):
        if not self.__filename:
            return global_filters
        return self.__parse_filters()

    # check required fields
    @general_exception
    def __parse_req(self, sec, basename):
        if basename in filters_req:
            for req in filters_req[basename]:
                if sec.get(req) == None:
                    return False
                elif filters_req[basename][req] == None:
                    continue
                elif sec[req] not in filters_req[basename][req]:
                    return False
        return True

    # values parsing
    @general_exception
    def __parse_value(self, sec, key, value):
        if value == "true" or value == "True":
            sec[key] = True
        elif value == "false" or value == "False":
            sec[key] = False
        elif re.search(",", value):
            sec[key] = re.split("\s*,\s*", value)
        else:
            sec[key] = [value]
        return sec

    # parse sections
    @general_exception
    def __parse_loop(self, parser, sec, name, refname=None):
        # define referer name
        if not refname:
            refname = name

        # get subsections
        keys = [refname]
        if re.search("\.", refname):
            keys = re.split("\.", refname)
        basename = keys[0]

        # create subsections
        curname = refname
        cursec = sec
        for key in keys:
            if cursec.get(key) == None:
                cursec[key] = {}
            cursec = cursec[key]

        # content parsing
        for key, value in parser.items(name):
            if key == '_contentrefer':
                if value == name:
                    raise ParserException, ("filter file error on section %s" % refname)
                return self.__parse_loop(parser, sec, value, name)
            elif re.search("\.", key) and ((name in filters_split) or (basename in filters_split)):
                skey = re.split("\.", key)
                if cursec.get(skey[0]) == None:
                    cursec[skey[0]] = {}
                cursec[skey[0]] = self.__parse_value(cursec[skey[0]], skey[1], value)
            else:
                cursec = self.__parse_value(cursec, key, value)

        # check required fields
        if (self.__parse_req(cursec, basename) == False):
            raise ParserException, ("filter file error on section %s" % refname)
        return sec

    # parse filters file
    @general_exception
    def __parse_filters(self):
        parser = SafeConfigParser()
        parser.read(self.__filename)
        sec = {}
        for name in parser.sections():
            sec = self.__parse_loop(parser, sec, name)
        return tools.dict_merging(global_filters, sec)
