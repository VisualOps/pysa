#!/usr/bin/python
'''
Main file

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

from optparse import *
import logging
import re

from pysa.tools import tools
from pysa.preprocessing import preprocessing
from pysa.exception import *
from pysa.madeira import *

from pysa.filter.parser import fparser
from pysa.scanner.scanner_handler import module_scan
from pysa.puppet.puppet_converter import puppet_converter
from pysa.puppet.puppet_build import puppet_build
from pysa.puppet.puppet_objects import *


# global defines
USAGE = 'usage: %prog [-hpq] [-m module_name] [-o output_path] [-f filter_config_path] [-l {-u madeira_username}|{-i madeira_id}]'
VERSION_NBR = '0.2.1a4'
VERSION = '%prog '+VERSION_NBR

# logger settings
LOG_FILENAME = '/tmp/scanner.log'
LOG_FORMAT = '%(asctime)s-%(name)s-%(levelname)s-%(message)s'
def __log(lvl):
    level = logging.getLevelName(lvl)
    formatter = logging.Formatter(LOG_FORMAT)
    handler = logging.StreamHandler()
    logger = logging.getLogger()
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)


# scanner class
class scanner():
    def __init__(self, filters=None):
        self.resources = None
        self.filters = filters
    
    @general_exception
    # get resource from different modules
    def scan(self):
        logging.info('Scanner.scan(): start scanning')
        self.resources = module_scan(self.filters if self.filters else None)
    
    @general_exception
    # generate puppet files
    def show_puppet(self, path, module):
        logging.info('Scanner.show_puppet(): Puppet files will be stored in path: %s' % path)
        self.preproc = preprocessing(PUPPET_OBJ_MAKER, self.resources)
        puppetdict = puppet_converter(self.preproc.run(), self.filters)
        p = puppetdict.run()
        puppet = puppet_build(p, path, module)
        puppet.run()

# print header
def print_header():
    print "Pysa v"+VERSION_NBR
    print '''

    pysa - reverse a complete computer setup
    Copyright (C) 2013  MadeiraCloud Ltd.

Thank you for using pysa!
Be aware that you are using an early-build (alpha release).
To provide the best result, ensure that you are not using an outdated version (check out http://github.com/MadeiraCloud/pysa or http://pypi.python.org/pypi/Pysa to get the latest version).
Please don't hesitate to report any bugs, requirements, advice, criticisms, hate or love messages to either pysa-user@googlegroups.com for public discussions and pysa@mc2.io for private messages.
'''

# option parser - user handler
def check_user(option, opt_str, value, parser):
    if parser.values.user or parser.values.id:
        setattr(parser.values, option.dest, True)
    else:
        raise OptionValueError("can't use -l without -u or -i (see usage)")

# option parser
def main_parse():
    parser = OptionParser(usage=USAGE, version=VERSION)
    parser.add_option("-p", "--puppet", action="store_true", dest="puppet", default=False,
                      help="scan packages and generate the puppet files"
                      )
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False,
                      help="operate quietly"
                      )
    parser.add_option("-m", "--module", action="store", dest="module", default="pysa",
                      help="define module name"
                      )
    parser.add_option("-o", "--output", action="store", dest="output", default="./output",
                      help="Path to output"
                      )
    parser.add_option("-f", "--filter", action="store", dest="filter",
                      help="add some user filters"
                      )
    parser.add_option("-l", "--madeira", action="callback", callback=check_user, dest='l',
                      help="post data to madeira"
                      )
    parser.add_option("-u", "--user", "--username", action="store", dest='user',
                      help="madeira username"
                      )
    parser.add_option("-i", "--id", action="store", dest='id',
                      help="identify user id"
                      )
    return parser.parse_args()

def main():
    # print header
    print_header()

    # options parsing
    options, args = main_parse()
    __log(('ERROR' if options.quiet else 'INFO'))
    output = (options.output if options.output else "./output")
    module = (options.module if options.module else "pysa")
    user = (options.user if options.user else None)
    uid = (options.id if options.id else None)

    # filters parsing
    filter_parser = fparser(options.filter if options.filter else None)
    filters = filter_parser.run()

    # scan for files
    s = scanner(filters)
    s.scan()
    # generate puppet output
    if options.puppet:
        s.show_puppet(output, module)

    # save to madeira accound
    if options.l:
        m = madeira(user, uid, output, module)
        m.send()

    
if __name__ == '__main__':
    main()
