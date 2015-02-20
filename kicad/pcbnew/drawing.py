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
import cmath
import math

pcbnew = __import__('pcbnew')

from kicad.pcbnew import layer as pcbnew_layer
from kicad.point import Point
from kicad import units


def _get_board_layer(board, layer_name):
    if board:
        return board.get_layer(layer_name)
    else:
        return pcbnew_layer.get_std_layer(layer_name)


class Segment(object):
    def __init__(self, start, end, layer='F.SilkS', width=0.15, board=None):
        self._line = pcbnew.DRAWSEGMENT(board and board.native_obj)
        self._line.SetShape(pcbnew.S_SEGMENT)
        self._line.SetStart(Point.native_from(start))
        self._line.SetEnd(Point.native_from(end))
        self._line.SetLayer(_get_board_layer(board, layer))
        self._line.SetWidth(int(width * units.DEFAULT_UNIT_IUS))

    @property
    def native_obj(self):
        return self._line


class Circle(object):
    def __init__(self, center, radius, layer, width, board=None):
        self._circle = pcbnew.DRAWSEGMENT(board and board.native_obj)
        self._circle.SetShape(pcbnew.S_CIRCLE)
        self._circle.SetCenter(Point.native_from(center))
        start_coord = Point.native_from(
            (center[0], center[1] + radius))
        self._circle.SetArcStart(start_coord)
        self._circle.SetLayer(_get_board_layer(board, layer))
        self._circle.SetWidth(int(width * units.DEFAULT_UNIT_IUS))

    @property
    def native_obj(self):
        return self._circle


class Arc(object):
    def __init__(self, center, radius, start_angle, stop_angle, layer, width,
                 board=None):
        start_coord = radius * cmath.exp(math.radians(start_angle - 90) * 1j)
        start_coord = Point.native_from((start_coord.real, start_coord.imag))

        angle = stop_angle - start_angle
        self._arc = pcbnew.DRAWSEGMENT(board and board.native_obj)
        self._arc.SetShape(pcbnew.S_ARC)
        self._arc.SetCenter(Point.native_from(center))
        self._arc.SetArcStart(start_coord)
        self._arc.SetAngle(angle * 10)
        self._arc.SetLayer(_get_board_layer(board, layer))
        self._arc.SetWidth(int(width * units.DEFAULT_UNIT_IUS))

    @property
    def native_obj(self):
        return self._arc
