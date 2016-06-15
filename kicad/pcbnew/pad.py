#  Copyright 2016 Hasan Yavuz Ozderya <hy@ozderya.net>
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
from kicad import units
from kicad import Size
from kicad.pcbnew.item import HasPosition
from enum import IntEnum

class DrillShape(IntEnum):
    Circle = pcbnew.PAD_DRILL_SHAPE_CIRCLE
    Oval = pcbnew.PAD_DRILL_SHAPE_OBLONG

class Pad(HasPosition, object):
    def __init__(self):
        # TODO: add initialization parameters for `Pad`
        pass

    @property
    def native_obj(self):
        return self._obj

    @staticmethod
    def wrap(instance):
        """Wraps a C++ api PAD object, and returns a `Pad`."""
        return kicad.new(Pad, instance)

    @property
    def drillShape(self):
        return DrillShape(self._obj.GetDrillShape())

    @drillShape.setter
    def drillShape(self, value):
        """Value should be `DrillShape`."""
        self._obj.SetDrillShape(value)

    @property
    def drill(self):
        """Drill size. If pad shape is circle returns a single float, if drill
        shape is oval, returns `Size`."""
        size = Size.wrap(self._obj.GetDrillSize())

        if self.drillShape == DrillShape.Circle:
            return size.width
        else: # oval
            return size

    @drill.setter
    def drill(self, value):
        """Sets the drill size. If value is a single float or int, pad drill
        shape is set to circle, if input is a tuple of (x, y) drill
        shape is set to oval."""
        if isinstance(value, tuple):
            self.drillShape = DrillShape.Oval
            if not isinstance(value, Size):
                value = Size(value[0], value[1])

            self._obj.SetDrillSize(value.native_obj)

        else: # value is a single number/integer
            drillShape = DrillShape.Circle
            self._obj.SetDrillSize(Size(value, value).native_obj())
