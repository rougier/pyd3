# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import unittest
from pyd3.color import Color
from pyd3 import interpolate


class test_number(unittest.TestCase):

    def test_1(self):
        """
        interpolate_rgb(a, b) converts a and b to RGB colors
        """
        i = interpolate.rgb( Color("steelblue"), Color("brown"))
        self.assertEqual(i(0), Color("steelblue"))
        self.assertEqual(i(1), Color("brown"))

    def test_2(self):
        """
        interpolate_rgb(a, b) interpolates in RGB and returns a hexadecimal string
        """
        i = interpolate.rgb(Color("steelblue"), Color("#f00"))
        self.assertEqual(i(.2), Color("#6b6890"))
    
if __name__ == "__main__":
    unittest.main()
