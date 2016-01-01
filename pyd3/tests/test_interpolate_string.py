# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import unittest
from pyd3 import interpolate

class test_string(unittest.TestCase):

    def test_1(self):
        """
        string(a, b) interpolates matching numbers in a and b.
        """
        i = interpolate.string(" 10/20 30", "50/10 100 ")
        self.assertEqual( i(0.2), "18/18 44 ")
        self.assertEqual( i(0.4), "26/16 58 ")

    def test_3(self):
        """
        string(a, b) preserves non-numbers in string b.
        """
        i = interpolate.string(" 10/20 30", "50/10 foo ")
        self.assertEqual( i(0.2), "18/18 foo ")
        self.assertEqual( i(0.4), "26/16 foo ")

    def test_4(self):
        """
        string(a, b) preserves non-matching numbers in string b.
        """
        i = interpolate.string(" 10/20 foo", "50/10 100 ")
        self.assertEqual( i(0.2), "18/18 100 ")
        self.assertEqual( i(0.4), "26/16 100 ")

    def test_5(self):
        """
        string(a, b) preserves equal-value numbers in both strings.
        """
        i = interpolate.string(" 10/20 100 20", "50/10 100, 20 ")
        self.assertEqual( i(0.2), "18/18 100, 20 ")
        self.assertEqual( i(0.4), "26/16 100, 20 ")

    def test_6(self):
        """
        string(a, b) interpolates decimal notation correctly.
        """
        i = interpolate.string("1.", "2.")
        self.assertEqual( i(0.5), "1.5")

    def test_7(self):
        """
        string(a, b) interpolates exponent notation correctly.
        """
        self.assertEqual(interpolate.string("1e+3", "1e+4")(0.5), "5500")
        self.assertEqual(interpolate.string("1e-3", "1e-4")(0.5), "0.00055")
        self.assertEqual(interpolate.string("1.e-3", "1.e-4")(0.5), "0.00055")
        self.assertEqual(interpolate.string("-1.e-3", "-1.e-4")(0.5), "-0.00055")
        self.assertEqual(interpolate.string("+1.e-3", "+1.e-4")(0.5), "0.00055")
        self.assertEqual(interpolate.string(".1e-2", ".1e-3")(0.5), "0.00055")

    def test_8(self):
        """
        string(a, b) with no numbers, returns the target string.
        """
        self.assertEqual(interpolate.string("foo", "bar")(.5), "bar")
        self.assertEqual(interpolate.string("foo", "")(.5), "")
        self.assertEqual(interpolate.string("", "bar")(.5), "bar")
        self.assertEqual(interpolate.string("", "")(.5), "")

    def test_9(self):
        """
        string(a, b) with two numerically-equivalent numbers, returns the default
        format.
        """
        self.assertEqual(interpolate.string("top: 1000px;", "top: 1e3px;")(.5),
                         "top: 1000px;")
        self.assertEqual(interpolate.string("top: 1e3px;", "top: 1000px;")(.5),
                         "top: 1000px;")

if __name__ == "__main__":
    unittest.main()
