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


import kicad
from kicad import Point


WRAPPED_CLASSES = [pcbnew.MODULE]


def wrap(instance):
    if type(instance) is pcbnew.MODULE:
        return kicad.new(Module, instance)


class Module(object):
    def __init__(self, reference=None, position=None, board=None):
        self._obj = pcbnew.MODULE(board.native_obj)
        if reference:
            self.reference = reference
        if position:
            self.position = position
        if board:
            board.add(self)

    @property
    def native_obj(self):
        return self._obj

    @property
    def reference(self):
        return self._obj.GetReference()

    @reference.setter
    def reference(self, value):
        self._obj.SetReference(value)

    @property
    def position(self):
        return Point.wrap(self._obj.GetPosition())

    @position.setter
    def position(self, value):
        self._obj.SetPosition(Point.native_from(value))

    def copy(self, ref, position=None, board=None):
        """Create a copy of an existing module on the board"""
        _module = pcbnew.MODULE(board)
        _module.Copy(self._obj)
        module = wrap(_module)
        module.reference = ref
        if position:
            module.position = position
        if board:
            board.add(module)
        return module
