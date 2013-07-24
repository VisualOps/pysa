'''
Generate salt manifests

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

# salt generation class
class SaltBuild():
    def __init__(self, input_dict, output_path, module_name):
        self.__module_name = module_name
        self.__input_dict = input_dict
        self.__output_container = Output()
        self.__output_path = output_path+'/'+self.__module_name
        self.__curent_manifest = None
        self.__curent_state = None
        self.__curent_name = None

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
            Tools.write_in_file(self.__output_path+'/'+manifest_fname+'.sls',
                                self.__output_container.dump(manifest_name))

    # init file generation
    @GeneralException
    def __create_init_file(self):
        self.__output_container.add(None, "include:\n")
        for manifest in self.__output_container.list():
            if not manifest: continue
            self.__output_container.add(None, "  - %s.%s\n"%(self.__module_name,manifest))

    # content writing
    @GeneralException
    def __write_content(self, key, val, tab):
        if (self.__curent_manifest in FILE_CLASS) and key == 'source':
            name = self.__input_dict[self.__curent_manifest][self.__curent_state][self.__curent_name]['name']
            filename = "%s" % (('/' if name[0] != '/' else '')+name)
            Tools.write_in_file(self.__output_path+'/templates'+filename, val)
            val = "salt://%s" % (self.__module_name+'/templates'+filename)
        self.__output_container.add(self.__curent_manifest, "%s"%(val))

    # section generation (recursive)
    @GeneralException
    def __create_section(self, key, val, tab):
        if (key in NULL) or (val == None): return
        self.__output_container.add(self.__curent_manifest, "%s- %s"%(tab,key))
        if val == MAIN_SECTION:
            self.__output_container.add(self.__curent_manifest, "\n")
        elif type(val) is dict:
            tab += "  "
            self.__output_container.add(self.__curent_manifest, ":\n")
            for sub_key in val:
                self.__create_section(sub_key, val[sub_key], tab)
        elif type(val) is list:
            tab += "  "
            self.__output_container.add(self.__curent_manifest, ":\n")
            for d in val:
                self.__create_section(d, MAIN_SECTION, tab)
        else:
            self.__output_container.add(self.__curent_manifest, ": ")
            self.__write_content(key, val, tab)
            self.__output_container.add(self.__curent_manifest, "\n")

    # global content generation for salt config file
    @GeneralException
    def __create_content(self, data, manifest, state, name):
        cur_data = data[manifest][state][name]
        self.__output_container.add(self.__curent_manifest, "%s:\n"%(name if name[0] != '-' else name[1:]))
        self.__output_container.add(self.__curent_manifest, "  %s:\n"%(state[len(ACTION_ID):]))
        for key in cur_data:
            self.__create_section(key, cur_data[key], "    ")

    # puppet file generation function
    @GeneralException
    def __generate(self, data):
        # global generation
        for manifest in sorted(data):
            Tools.l(INFO, "generation manifest %s" % (manifest), 'generate', self)
            self.__curent_manifest = manifest
            for state in sorted(data[manifest]):
                self.__curent_state = state
                Tools.l(INFO, "module state %s" % (state), 'generate', self)
                for name in sorted(data[manifest][state]):
                    self.__curent_name = name
                    Tools.l(INFO, "item %s" % (name), 'generate', self)
                    self.__create_content(data, manifest, state, name)
