'''
Created on 2013-04-19

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

@author: Michael
'''

from pysa.scanner.object.object_base import object_base


class process(object_base):

    def __init__(self, pid, owner, status, cpu, mem, cmd, ppid=None):
        self.pid    =   pid     # process id
        self.owner  =   owner
        self.status =   status  # D:uninterruptible sleep, R:runnable, S:sleeping, T:raced or stopped, Z:defunct process
        self.cpu    =   cpu     # cpu%
        self.mem    =   mem     # mem%
        self.cmd    =   cmd
        self.ppid   =   ppid    # parent pid
