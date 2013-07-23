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

from pysa.exception import *
from pysa.config import *
from pysa.tools import *
from pysa.output import Output

from pysa.puppet.converter import GLOBAL_SEC_EQ

# define quoted variables
QUOTED_AVOIDED_KEYS = ['content', 'before']
QUOTED_FORCED_KEYS = ['checksum', 'name', 'group', 'owner']
QUOTED_FORCED_CONTENT = ['\W', '\d']

# puppet generation class
class PuppetBuild():
    def __init__(self, input_dict, output_path, module_name):
        self.__quoted_regex = "%s" % ('|'.join(QUOTED_FORCED_CONTENT))
        self.__module_name = module_name
        self.__input_dict = input_dict
        self.__output_container = Output()
        self.__output_path = output_path+'/'+self.__module_name
        self.__curent_manifest = ''

    # main function
    @GeneralException
    def run(self):
        Tools.l(INFO, "running generation engine", 'run', self)
        self.__generate(self.__input_dict)
        self.__create_init_file()
        self.dump_in_files()
        Tools.l(INFO, "generation complete", 'run', self)
        return True

    # print the puppet files
    @GeneralException
    def dump(self):
        for manifest_name in self.__output_container.list():
            manifest_fname = (manifest_name if manifest_name else 'init')
            print "%s:\n%s\n\n" % (manifest_fname,
                                   self.__output_container.dump(manifest_name))

    # dump puppet file in variable
    @GeneralException
    def dump_in_var(self, data=''):
        for manifest_name in self.__output_container.list():
            manifest_fname = (manifest_name if manifest_name else 'init')
            data += ("%s:\n%s\n\n" % (manifest_fname,
                                      self.__output_container.dump(manifest_name)))
        return data

    # dump the puppet files into the right files
    @GeneralException
    def dump_in_files(self):
        for manifest_name in self.__output_container.list():
            manifest_fname = (manifest_name if manifest_name else 'init')
            Tools.write_in_file(self.__output_path+'/manifests/'+manifest_fname+'.pp',
                                self.__output_container.dump(manifest_name))

    # init file generation
    @GeneralException
    def __create_init_file(self):
        includes = ''
        for manifest_name in self.__output_container.list():
            if not manifest_name: continue
            includes += "include %s\n" % (manifest_name)
        content = ''
        for line in re.split('\n',
                             self.__output_container.dump()+'\n'+includes):
            if not line: continue
            content += re.sub(r'^', r'\n\t', line)
        self.__output_container.mod("class %s {\n%s\n}\n" % (self.__module_name, content))

    # particular case for the single instructions
    @GeneralException
    def __single_instruction(self, parent, sections, section_name, tab):
        if not parent:
            return tab
        for content in sections[section_name]:
            if section_name == GLOBAL_SEC_EQ['require']:
                if content not in parent: continue
            self.__output_container.add(self.__curent_manifest,
                                        "%s%s %s\n" % (tab,section_name[len(SINGLE_SEC):],content))
        return tab

    # quote required values
    @GeneralException
    def __add_quotes(self, key, val):
        return (("'%s'" % (re.sub('\'', '\\\'', val))
                 if (key not in QUOTED_AVOIDED_KEYS)
                 and ((key in QUOTED_FORCED_KEYS)
                      or (re.search(self.__quoted_regex, val)))
                 else val)
                if type(val) is str else val)

    # content writing
    @GeneralException
    def __write_content(self, section_name, label, optlabel, content):
        out = ''
        out_size = 0
        if (type(content) is list):
            for value in content:
                out += (", " if out_size else '')+"'%s'" % (value)
                out_size += 1
            if out_size:
                return "%s%s%s" % (("[" if out_size > 1 else ''),out,("]" if out_size > 1 else ''))
        elif (type(content) is dict):
            for value_type in content:
                for value in content[value_type]:
                    out += (", " if out_size else '') + "%s['%s']" % (value_type,value)
                    out_size += 1
            if out_size:
                return "%s%s%s" % (("[" if out_size > 1 else ''),out,("]" if out_size > 1 else ''))
        else:
            if (self.__curent_manifest in FILE_CLASS) and (label[0] != '-') and optlabel == 'content':
                filename = ('/' if label[0] != '/' else '')+label
                Tools.write_in_file(self.__output_path+'/templates'+filename, content)
                content = "template('%s')" % (self.__module_name+filename)
            return self.__add_quotes(optlabel, content)
        return None

    # global content generation for pupept config file
    @GeneralException
    def __create_content(self, parent, data, section_name, tab):
        Tools.l(INFO, "creating section %s" % (section_name.lstrip(VOID_EQ)), 'create_content', self)
        if section_name[:len(SINGLE_SEC)] == SINGLE_SEC:
             return self.__single_instruction(parent, data, section_name, tab)
        self.__output_container.add(self.__curent_manifest, "%s%s {\n" % (tab,section_name.lstrip(ACTION_ID)))
        for label in sorted(data[section_name]):
            if label in NULL:
                continue
            if label[0] != ACTION_ID:
                tab = Tools.tab_inc(tab)
                self.__output_container.add(self.__curent_manifest, "%s'%s':\n" % (tab,label))
            tab = Tools.tab_inc(tab)
            wrote = False
            for optlabel in sorted(data[section_name][label]):
                if (data[section_name][label][optlabel] not in NULL) and (optlabel[0] != ACTION_ID):
                    out = self.__write_content(section_name,
                                               label,
                                               optlabel,
                                               data[section_name][label][optlabel])
                    if out:
                        self.__output_container.add(self.__curent_manifest,
                                                    "%s%s%s => %s"%((",\n" if wrote else ''),tab,optlabel,out))
                        wrote = True
            if wrote and label != MAIN_SECTION:
                self.__output_container.add(self.__curent_manifest, ";\n")
            elif wrote and label == MAIN_SECTION:
                self.__output_container.add(self.__curent_manifest, "\n")
            tab = Tools.tab_dec(tab)
            if label[0] != ACTION_ID:
                tab = Tools.tab_dec(tab)
        self.__output_container.add(self.__curent_manifest, "%s}\n" % (tab))
        return tab

    # class generation method, applies the recursion
    @GeneralException
    def __create_class(self, parent, data, section_name, tab):
        Tools.l(INFO, "generation class %s" % (section_name), 'create_class', self)
        self.__output_container.add(self.__curent_manifest, "%sclass %s {\n" % (tab,section_name))
        tab = Tools.tab_inc(tab)
        # recursion here
        tab = self.__generate(data[section_name], data, tab)
        tab = Tools.tab_dec(tab)
        self.__output_container.add(self.__curent_manifest, "%s}\n%sinclude %s\n" % (tab,tab,section_name))
        return tab

    # puppet file generation function
    # recursive function
    @GeneralException
    def __generate(self, data, parent = None, tab=''):
        # adding Exec section
        if GLOBAL_SEC_EQ['Exec'] in data:
            tab = self.__create_content(parent, data, GLOBAL_SEC_EQ['Exec'], tab)
        # global generation
        for section_name in sorted(data):
            # avoid exception
            if section_name == GLOBAL_SEC_EQ['Exec']:
                continue
            # content found
            elif section_name[0] == ACTION_ID and self.__curent_manifest:
                tab = self.__create_content(parent, data, section_name, tab)
                continue
            # new class
            if not parent:
                self.__curent_manifest = section_name
                self.__output_container.add_dict(self.__curent_manifest)
            # recursion here
            tab = self.__create_class(parent, data, section_name, tab)
        return tab
