#  Copyright 2014 Piers Titus van der Torren <pierstitus@gmail.com>
#  Copyright 2015 Miguel Angel Ajo <miguelangel@ajo.es>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
pcbnew = __import__('pcbnew')
from kicad import *


class Module:
    def __init__(self, reference=None, position=None, board=None,
                 module=None):
        if module:
            self._module = module
        else:
            self._module = pcbnew.MODULE(board)
            if reference:
                self.reference = reference
            if position:
                self.position = position
            if board:
                board.add(self)

    @property
    def native_obj(self):
        return self._module

    @property
    def reference(self):
        return self._module.GetReference()

    @reference.setter
    def set_reference(self, value):
        self._module.SetReference(value)

    @property
    def position(self):
        return Point(self._module.GetPosition())

    @position.setter
    def set_position(self, value):
        self._module.SetPosition(Point._from_tuple(value))
