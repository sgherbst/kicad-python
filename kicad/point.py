#  Copyright 2015 Miguel Angel Ajo Pelayo <miguelangel@ajo.es>
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

#TODO(mangelajo): we will have to come with something more generic
#                 or make the wx* objects compatible across bindings
pcbnew = __import__('pcbnew')
import cmath

import kicad
from kicad import units


class Point(units.BaseUnitTuple):

    def __init__(self, x, y):
        self._class = Point
        self._obj = pcbnew.wxPoint(x * units.DEFAULT_UNIT_IUS,
                                   y * units.DEFAULT_UNIT_IUS)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Point(%g, %g)" % (self.x, self.y)

    @staticmethod
    def wrap(instance):
        wrapped_point = kicad.new(Point, instance)
        wrapped_point._class = Point
        return wrapped_point

    @staticmethod
    def build_from(t):
        return Point._tuple_to_class(t, Point)

    @staticmethod
    def native_from(t):
        return Point._tuple_to_class(t, Point).native_obj

    @property
    def native_obj(self):
        return self._obj

    def rotate(self, angle, around=(0, 0)):
        self.x, self.y = self._rotated(angle, around)

    def rotated(self, angle, around=(0, 0)):
        x, y = self._rotated(angle, around)
        return Point(x, y)

    def _rotated(self, angle, around=(0, 0)):
        """Rotate coordinate around another point"""
        around = Point.build_from(around)
        p0 = self - around
        coord = (p0.x + p0.y * 1j) * cmath.exp((angle / units.rad) * 1j)
        return (coord.real + around.x, coord.imag + around.y)
