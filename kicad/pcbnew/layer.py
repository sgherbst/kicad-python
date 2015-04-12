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

# dicts for converting layer name to id, used by _get_layer
_std_layer_dict = {pcbnew.BOARD_GetStandardLayerName(n): n
                   for n in range(pcbnew.LAYER_ID_COUNT)}
_std_layer_names = {s: n for n, s in _std_layer_dict.iteritems()}


def get_board_layer(board, layer_name):
    if board:
        return board.get_layer(layer_name)
    else:
        return get_std_layer(layer_name)


def get_std_layer(s):
    """Get layer id from layer name

    If it is already an int just return it.
    """
    return _std_layer_dict[s]


class LayerSet:
    def __init__(self, layers, board=None):
        self._board = board
        self._build_layer_set(layers)

    def _build_layer_set(self, layers):
        """Create LayerSet used for defining pad layers"""
        bitset = 0
        for layer_name in layers:
            if self._board:
                bitset |= 1 << self._board.get_layer(layer_name)
            else:
                bitset |= 1 << get_std_layer(layer_name)
        hexset = '{0:013x}'.format(bitset)
        self.lset = pcbnew.LSET()
        self.lset.ParseHex(hexset, len(hexset))


#def LayerSet(layerset):
#    mask = [c for c in layerset.FmtBin() if c in ('0','1')]
#    mask.reverse()
#    ids = [i for i, c in enumerate(mask) if c == '1']
#    return tuple(layer_names[i] for i in ids)
