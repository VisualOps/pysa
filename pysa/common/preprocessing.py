'''
Data preprocessing before modules

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

from common.tools import *
from common.exception import *
from common.config import FILE_CLASS

FILE_IDENT = FILE_CLASS + [
#    'sources',
    ]

# preprocesser
class preprocessing():
    def __init__(self, obj_maker, data=None):
        self.__obj_maker = obj_maker
        self.__data = data

    # action
    @general_exception
    def run(self, data=None):
        if data:
            self.__data = data
        if self.__data:
            self.__prepross_files()
        return self.__data

    # preprocessing on files section
    @general_exception
    def __prepross_files(self):
        tools.l(INFO, "preprocessing files", 'prepross_files', self)
        dds = self.__files_iter(self.__file_directory, FILE_IDENT)
        for file_item in dds:
            self.__data['dirs'] = tools.s_dict_merging(self.__data.get('dirs'), dds[file_item])
        self.__files_iter(self.__file_item_removal, ['dirs']+FILE_CLASS)
        tools.l(INFO, "preprocessing files done", 'prepross_files', self)

    # create config files directory
    @general_exception
    def __file_directory(self, container, file_item, files, file, files_l):
        if container.get(file_item) == None:
            container[file_item] = {}
        fp = files[file]['path']
        drs = tools.get_recurse_path(os.path.dirname(fp))
        for dr in drs:
            if (dr == '/') or (("-%s"%dr) in container[file_item]):
                continue
            container[file_item]["-%s"%dr] = self.__obj_maker['file'](dr)
        return container

    # remove items
    @general_exception
    def __file_item_removal(self, container, file_item, files, file, files_l):
        r_files_l = files_l[:]
        r_files_l.reverse()
        for consumed in r_files_l:
            if consumed == file_item:
                break
            elif self.__data.get(consumed):
                flag = None
                for f in self.__data[consumed]:
                    path = self.__data[consumed][f]['path']
                    if path == files[file]['path']:
                        flag = f
                        break
                if flag:
                    self.__data[consumed].pop(flag)
        return container

    # iterate over files
    @general_exception
    def __files_iter(self, action, files_l):
        container = {}
        for file_item in files_l:
            files = (dict(self.__data[file_item].items()) if self.__data.get(file_item) else {})
            for file in files:
                container = action(container, file_item, files, file, files_l)
        return container
