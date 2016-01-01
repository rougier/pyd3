# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import unittest
from pyd3 import interpolate

class test_number(unittest.TestCase):

    def test_1(self):
        """
        interpolate_number(a, b) interpolates between two numbers a and b.
        """

        i = interpolate.number(10, 42)
        self.assertAlmostEqual(i(0.0), 10.0, delta=1e-6)
        self.assertAlmostEqual(i(0.1), 13.2, delta=1e-6)
        self.assertAlmostEqual(i(0.2), 16.4, delta=1e-6)
        self.assertAlmostEqual(i(0.3), 19.6, delta=1e-6)
        self.assertAlmostEqual(i(0.4), 22.8, delta=1e-6)
        self.assertAlmostEqual(i(0.5), 26.0, delta=1e-6)
        self.assertAlmostEqual(i(0.6), 29.2, delta=1e-6)
        self.assertAlmostEqual(i(0.7), 32.4, delta=1e-6)
        self.assertAlmostEqual(i(0.8), 35.6, delta=1e-6)
        self.assertAlmostEqual(i(0.9), 38.8, delta=1e-6)
        self.assertAlmostEqual(i(1.0), 42.0, delta=1e-6)

if __name__ == "__main__":
    unittest.main()
