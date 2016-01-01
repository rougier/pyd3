# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import unittest
from pyd3 import interpolate

class test_number(unittest.TestCase):

    def test_1(self):
        """
        interpolate_round(a, b) interpolates between two numbers a and b, and then
        rounds.
        """

        i = interpolate.round(10, 42)
        self.assertEqual(i(0.0), 10)
        self.assertEqual(i(0.1), 13)
        self.assertEqual(i(0.2), 16)
        self.assertEqual(i(0.3), 20)
        self.assertEqual(i(0.4), 23)
        self.assertEqual(i(0.5), 26)
        self.assertEqual(i(0.6), 29)
        self.assertEqual(i(0.7), 32)
        self.assertEqual(i(0.8), 36)
        self.assertEqual(i(0.9), 39)
        self.assertEqual(i(1.0), 42)

    def test_2(self):
        """ round(a, b) does not pre-round a and b """
        i = interpolate.round(2.6, 3.6)
        self.assertEqual(i(0.6), 3)

if __name__ == "__main__":
    unittest.main()
