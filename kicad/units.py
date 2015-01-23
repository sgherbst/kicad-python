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

import kicad.exceptions


MM = 0
INCHES = 1
IU = 2
CONTEXT = -1


def units(type_of_units):
    """Helper to build unit contexts to work with kicad objects.

    This helper is used to define a context for units, to avoid
    explicitly passing the type of unit on every call when we
    want to work with a certain unit.

    Example:
        with unit(MM):
            point = Point(1.0, 1.0)
            size = Size(1.0, 2.0)
    """
    return _UnitContext(type_of_units)


def with_units(type_of_units):
    """Decorator to declare which units a function will use.

    This helper is used to define the unit context for a certain
    function when manipulating or creating kicad objects.

    Example:
        @with_units(MM)
        def my_function(pcb):
            pcb.new_module("M1", position=Point(50, 50))
    """

    def units_decorator(function):
        def wrapper(*args, **kwargs):
            with units(type_of_units):
                function(*args, **kwargs)
        return wrapper
    return units_decorator


def current_units():
    return _UnitContext.current_units()


class _UnitContext:
    context_stack = []

    def __init__(self, type_of_unit):
        self.unit = type_of_unit

    @staticmethod
    def current_units():
        try:
            return _UnitContext.context_stack[-1]
        except IndexError:
            raise kicad.exceptions.NoDefaultUnits(
                "You're trying to use units without a context/default, "
                "please decorate your main @with_units(xxx) or use "
                "with units(xxx): in your code")

    def __enter__(self):
        _UnitContext.context_stack.append(self.unit)

    def __exit__(self, type, value, traceback):
        _UnitContext.context_stack.pop()
