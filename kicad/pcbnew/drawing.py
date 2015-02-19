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
from kicad.pcbnew import layer as pcbnew_layer
from kicad.point import Point
from kicad import units


class Segment(object):
    def __init__(self, start, end, layer='F.SilkS', width=0.15, board=None):
        self._line = pcbnew.DRAWSEGMENT(board and board.native_obj)
        self._line.SetShape(pcbnew.S_SEGMENT)
        self._line.SetStart(Point.from_tuple(start).native_obj)
        self._line.SetEnd(Point.from_tuple(end).native_obj)
        if board:
            self._line.SetLayer(board.get_layer(layer))
        else:
            self._line.SetLayer(pcbnew_layer.get_std_layer(layer))

        self._line.SetWidth(int(width * units.DEFAULT_UNIT_IUS))

    @property
    def native_obj(self):
        return self._line


class Circle(object):
    pass


class Arc(object):
    pass
