import unittest

from kicad import *


class TestUnits(unittest.TestCase):

    def test_with_units(self):
        with units(MM):
            self.assertEqual(current_units(), MM)
            with units(INCHES):
                self.assertEqual(current_units(), INCHES)
            self.assertEqual(current_units(), MM)

    @with_units(MM)
    def _decorated_test(self):
        self.assertEqual(current_units(), MM)

    def test_with_and_decorator(self):
        with units(INCHES):
            self.assertEqual(current_units(), INCHES)
            self._decorated_test()
            self.assertEqual(current_units(), INCHES)
