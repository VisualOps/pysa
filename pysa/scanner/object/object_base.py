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

import re


class ObjectBase(object):

    def prase(self):
        format_object = {}
        for attr in dir(self):
            if type(eval("self.%s" % attr)) in (str, int, dict, list, unicode) and not attr.startswith('_') and attr not in ['primarykey', 'primaryvalue']:
                format_object[attr] = eval("self.%s" % attr)
        return format_object

    @property
    def primarykey(self):
        pk = {
            'Package'   :   'name',
            'File'      :   'path',
            'User'      :   'name',
            'Service'   :   'name',
            'Repository':   'path',
            'Group'     :   'name',
            'Cron'      :   'name',
            'Host'      :   'name',
            'Mount'     :   'device',
            'SSHKey'    :   'name',
            'Source'    :   'path',
            'Process'   :   'pid'
        }

        return pk.get(self.__class__.__name__)

    @property
    def primaryvalue(self):
        return getattr(self, self.primarykey)

    def attr_filter(self, attr_rules):
        """
        attribute filter
        """

        if not attr_rules: return False

        # ignore rule's case
        type_list = [ i for i in attr_rules.keys() if i.upper()==(self.__class__.__name__).upper() ]
        if not type_list: return False

        the_type = type_list[0]
        for (attr, rules) in attr_rules[the_type].items():
            if not hasattr(self, attr): continue

            # get the object's attribute value
            value = getattr(self, attr)

            # ignore the null attribute value
            if value is None or not value: continue

            for rule in rules:
                if isinstance(value, list):    # list value
                    if all(isinstance(i, str) for i in value) or all(isinstance(i, unicode) for i in value):
                        if len([ m.group(0) for i in value for m in [re.match("%s$"%rule, i)] if m ])>0: return True
                elif isinstance(value, str) or isinstance(value, unicode):    # string
                    if re.search(rule, value):  return True
        return False

    def add_filter(self, add_rules):
        """
        addition filter
        """

        if not add_rules: return

        type_list = [ i for i in add_rules.keys() if i.upper()==(self.__class__.__name__).upper() ]
        if not type_list: return False

        the_type = type_list[0]
        for attr in add_rules[the_type]:
            # check whether has the attribute
            if not hasattr(self, attr): continue

            values = add_rules[the_type][attr]
            # global setting
            if isinstance(values, str) or isinstance(values, unicode):
                setattr(self, attr, values)
            elif isinstance(values, list):
                setattr(self, attr, values[0])
            # single setting
            elif isinstance(values, dict):
                for value in values:
                    if getattr(self, attr) == value:    # check whether the object
                        rules = values[value]
                        # update
                        for (add_attr, add_value) in rules.items():
                            if hasattr(self, add_attr) and len(add_value)>0:
                                setattr(self, add_attr, add_value[0])
