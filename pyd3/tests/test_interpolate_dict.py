# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import unittest
from pyd3 import interpolate

class test_number(unittest.TestCase):

    def test_1(self):
        """
        interpolate_dict(a, b) interpolates defined elements in a and b
        """

        i = interpolate.dict({"value": 2}, {"value": 4})
        self.assertEqual(i(.5), {"value": 3})
        
    def test_2(self):
        """
        interpolate_dict(a, b) merges non-shared properties
        """

        i = interpolate.dict({"foo": 2         },
                             {"foo": 4, "bar":4})
        self.assertEqual(i(.5), {"foo": 3, "bar": 4})
        
        i = interpolate.dict({"foo": 2, "bar":4},
                             {"foo": 4         })
        self.assertEqual(i(.5), {"foo": 3, "bar": 4})
        
    def test_3(self):
        """
        interpolate_dict(a, b)  interpolates nested dicts and list
        """
        i = interpolate.dict( {"foo": [2, 12]},
                              {"foo": [4, 24]})
        self.assertEqual(i(.5), {"foo": [3, 18]})

        i = interpolate.dict( {"foo": {"bar": [2, 12]}},
                              {"foo": {"bar": [4, 24]}})
        self.assertEqual(i(.5), {"foo": {"bar": [3, 18]}})
        
    def test_4(self):
        """
        interpolate_dict(a, b) interpolates color properties as rgb
        """

        i = interpolate.dict({"bg": "red"}, {"bg": "green"})
        self.assertEqual(i(.5), {"bg": "#804000"})
        
                    
if __name__ == "__main__":
    unittest.main()
