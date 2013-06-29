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

from pysa.tools import *
from pysa.exception import *


# filter actions
class filter():
    def __init__(self, filters):
        self.f = filters

    # preprocessing on packages section
    @general_exception
    def update_package(self, package, pkg_name, update):
        tools.l(INFO, "selection update packages", 'update_package', self)
        if (not self.f) or (not self.f.get('update')):
            return package
        mode = (self.f['update']['_update'] if self.f['update'].get('_update') else False)
        excp = self.f['update'].get('except')
        if self.exception_filter(mode, excp, pkg_name, ["*", ".*"]):
            package['version'] = update
        return package

    # item replacement
    @general_exception
    def item_replace(self, gclass, key, val, name, eq = None):
        if not self.f:
            return val        
        global1 = self.f.get('replace')
        global2 = (global1.get(gclass) if global1 else None)
        section = (global2.get(key) if global2 else None)

        replacelist = tools.dict_merging(tools.dict_merging(global1, global2), section)
        if not replacelist:
            return val
 
        mode = (replacelist.pop('_replaceall') if replacelist.get('_replaceall') != None else True)
        excp = (replacelist.pop('_except') if replacelist.get('_except') != None else None)

        replacelist = tools.dict_cleaner(replacelist)
        if not replacelist:
            return val
        
        if (excp == None
            or self.exception_filter(mode, excp, name, eq)):
            for i in replacelist:
                c = val
                for data in replacelist[i]:
                    if (type(val) != list) and (type(val) != dict):
                        val = re.sub("%s" % (data),
                                     "%s" % (i),
                                     "%s" % (val))
                if c != val:
                    tools.l(INFO,
                            "values updated for item %s in section %s"
                            % (name, key),
                            'item_replace',
                            self)
        return val

    # apply filter, replace: ["old", "new"]
    @general_exception
    def exception_filter(self, mode, exceptions, value, exprep = None):
        if (exceptions == None and mode == True):
            return True
        elif (exceptions == None and mode == False):
            return False
        fl = False
        for name in exceptions:
            name = "%s$" % (name)
            if re.match((name.replace(exprep[0], exprep[1]) if exprep else name), value):
                fl = True
                break
        if (((mode == True) and (fl == False))
            or ((mode == False) and (fl == True))):
            return True
        return False
