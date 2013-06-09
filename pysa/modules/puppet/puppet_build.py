'''
Generate puppet scripts

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

import re

from common.exception import *
from common.config import *
from common.tools import *
from common.output import output

from modules.puppet.puppet_converter import GLOBAL_SEC_EQ

# define quoted variables
QUOTED_AVOIDED_KEYS = ['content', 'before']
QUOTED_KEYS = ['checksum', 'name', 'group', 'owner']
QUOTED_CONTENT = ['\W', '\d']

# puppet generation class
class puppet_build():
    def __init__(self, class_dict, output_path, module):
        self.__prepross = [
#            [GLOBAL_SEC_EQ['order'], self.__order],
            [GLOBAL_SEC_EQ['Exec'], self.__content],
            ]

        self.__quoted_regex = "%s" % ('|'.join(QUOTED_CONTENT))
        self.__module_name = module
        self.__c = output()
        self.__class_dict = class_dict
        self.__output_path = output_path+'/'+self.__module_name
        self.__prepross_list = []
        for i in self.__prepross:
            self.__prepross_list.append(i[0])

    # main function
    @general_exception
    def run(self):
        tools.l(INFO, "running generation engine", 'run', self)
        self.__generate(self.__class_dict)
        self.__init_gen()
        self.dump_in_files()
        tools.l(INFO, "complete.", 'run', self)
        return True

    # print the puppet files
    @general_exception
    def dump(self):
        for c in self.__c.list():
            print "%s:\n%s\n\n" % ((c if c else 'init'),self.__c.dump(c))

    # dump puppet file in variable
    @general_exception
    def dump_in_var(self, data=''):
        for c in self.__c.list():
            data += ("%s:\n%s\n\n" % ((c if c else 'init'),self.__c.dump(c)))
        return data

    # dump the puppet files into the right files
    @general_exception
    def dump_in_files(self):
        for c in self.__c.list():
            tools.write_in_file(self.__output_path+'/manifests/'+(c if c else 'init')+'.pp', self.__c.dump(c))

    # init file generation
    @general_exception
    def __init_gen(self):
        inc=''
        for c in self.__c.list():
            inc += ("include %s\n" % (c) if c else '')
        tab = re.split('\n', self.__c.dump()+'\n'+inc)
        s=''
        for i in tab:
            s += (re.sub(r'^', r'\n\t', i) if i else '')
        self.__c.mod("class %s {\n%s\n}\n" % (self.__module_name, s))

#    # particular case for the variable order (define the execution order)
#    @general_exception
#    def __order(self, parent, data, index, output, tab):
#        if len(data[index]) <= 1:
#            tools.l(INFO, "no order written, only one class", 'order', self)
#            return tab
#        f = 0
#        for content in data[index]:
#            self.__c.add(output, (' -> ' if f else tab)+"Class['%s']" % (content))
#            f += 1
#        self.__c.add(output, ('\n' if f else ''))
#        return tab

    # particular case for the single instructions
    @general_exception
    def __single_instruction(self, parent, data, index, output, tab):
        if not parent:
            return tab
        for content in data[index]:
            if index == GLOBAL_SEC_EQ['require']:
                if content not in parent:
                    continue
            self.__c.add(output, tab+"%s %s\n" % (index[len(SINGLE_EQ):],content))
        return tab

    # quote required values
    @general_exception
    def __quote_values(self, key, val):
        return (("'%s'" % (re.sub('\'', '\\\'', val))
                 if (key not in QUOTED_AVOIDED_KEYS)
                 and ((key in QUOTED_KEYS)
                      or (re.search(self.__quoted_regex, val)))
                 else val)
                if type(val) is str else val)

    # content writing
    @general_exception
    def __content_writing(self, output, sectype, label, optlabel, content):
        i = 0
        s = ''
        if (type(content) is list):
            tmp_s = ''
            for sec in content:
                tmp_s += (", " if i else '')+"'%s'" % (sec)
                i += 1
            if i > 0:
                s += ("[" if i > 1 else '')+tmp_s+("]" if i > 1 else '')
            else: s = None
        elif (type(content) is dict):
            tmp_s = ''
            for sec in content:
                for d in content[sec]:
                    tmp_s += (", " if i else '') + "%s['%s']" % (sec,d)
                    i += 1
            if i > 0:
                s += ("[" if i > 1 else '')+tmp_s+("]" if i > 1 else '')
            else: s = None
        else:
            if (sectype == "_file") and (label[0] != '-') and optlabel == 'content':
                tools.write_in_file(self.__output_path+'/templates'+('/' if label[0] != '/' else '')+label,
                                    content)
                content = ("template('%s')" % (self.__module_name+('/' if label[0] != '/' else '')+label))
            s += "%s" % self.__quote_values(optlabel, content)
        return s

    # global content generation for pupept config file
    @general_exception
    def __content(self, parent, data, index, output, tab):
        tools.l(INFO, "creating section %s" % (index.lstrip(VOID_EQ)), 'content', self)
        if index[:len(SINGLE_EQ)] == SINGLE_EQ:
            return self.__single_instruction(parent, data, index, output, tab)
        self.__c.add(output, "%s%s {\n" % (tab,index.lstrip(VOID_EQ)))
        for label in sorted(data[index]):
            if label in NULL:
                continue
            elif label[0] != VOID_EQ:
                tab = tools.tab_inc(tab)
                self.__c.add(output, "%s'%s':\n" % (tab,label))
            f = 0
            tab = tools.tab_inc(tab)
            for optlabel in sorted(data[index][label]):
                if (data[index][label][optlabel] not in NULL) and (optlabel[0] != VOID_EQ):
                    s = self.__content_writing(output,
                                               index,
                                               label,
                                               optlabel,
                                               data[index][label][optlabel])
                    if s:
                        self.__c.add(output, (",\n" if f else '')+
                                     "%s%s => %s" % (tab, optlabel,s))
                        f = 1
            if f and label != VOID_EQ:
                self.__c.add(output, ";\n")
            elif f and label == VOID_EQ:
                self.__c.add(output, "\n")
            tab = tools.tab_dec(tab)
            if label[0] != VOID_EQ:
                tab = tools.tab_dec(tab)
        self.__c.add(output, "%s}\n" % (tab))
        return tab

    # class generation method, applies the recursion
    @general_exception
    def __object(self, parent, data, index, output, tab, level):
        tools.l(INFO, "generation class %s" % (index), 'object', self)
        self.__c.add(output, "%sclass %s {\n" % (tab,index))
        # recursion here
        tab = tools.tab_dec(self.__generate(data[index],
                                            data,
                                            output,
                                            tools.tab_inc(tab),
                                            level+1))
        self.__c.add(output, "%s}\n%sinclude %s\n" % (tab,tab,index))
        return tab

    # puppet file generation function
    # recursive function
    @general_exception
    def __generate(self, data, parent = None, output='', tab='', level=0):
        # preprocessing exceptions
        for t in self.__prepross:
            if t[0] in data and t[1]:
                tools.l(INFO, "adding %s condition" % (t[0]), 'generate', self)
                tab = t[1](parent, data, t[0], output, tab)
        # global generation
        for index in sorted(data):
            # particular cases needed to be at the beginning of a section
            if index in self.__prepross_list:
                continue
            # content found
            elif index[0] == VOID_EQ and output:
                tab = self.__content(parent, data, index, output, tab)
            # new class
            else:
                if (level == 0):
                    output = index
                    self.__c.add_dict(output)
                # recursion here
                tab = self.__object(parent, data, index, output, tab, level)
        return tab
