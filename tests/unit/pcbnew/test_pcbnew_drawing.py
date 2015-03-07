import unittest

from kicad import *
from kicad.pcbnew.drawing import *


class TestPcbnewDrawing(unittest.TestCase):
    def test_segment_from_native(self):
        native_segment = Segment((0, 0), (1, 1)).native_obj
        new_segment = Segment.from_native(native_segment)
        self.assertEqual(Segment, type(new_segment))
