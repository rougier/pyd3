# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import unittest
from pyd3 import interpolate

class test_number(unittest.TestCase):

    def test_1(self):
        """
        interpolate_list(a, b) interpolates defined elements in a and b
        """

        i = interpolate.list([2, 12], [4, 24])
        self.assertEqual(i(.5), [3, 18])

    def test_2(self):
        """
        interpolate_list(a, b) nested objects and arrays
        """
        i = interpolate.list([[2, 12]], [[4, 24]])
        self.assertEqual(i(.5), [[3, 18]])


    def test_3(self):
        """
        interpolate_list(a, b) merges non-shared elements
        """
        i = interpolate.list([[2, 12]], [[4, 24,12]])
        self.assertEqual(i(.5), [[3, 18, 12]])
        
        i = interpolate.list([[2, 12,12]], [[4, 24,12]])
        self.assertEqual(i(.5), [[3, 18, 12]])
        
if __name__ == "__main__":
    unittest.main()
