# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import unittest
import numpy as np
from pyd3 import scale

class test_scale_linear(unittest.TestCase):

    def test_1(self):
        """
        linear() has the expected defaults
        """
        s = scale.linear()
        self.assertEqual(s.domain, [0,1])
        self.assertEqual(s.range, [0,1])
        self.assertEqual(s.clamp, False)

    def test_2(self):
        """
        linear(x) maps a domain value x to a range value y"
        """

        s = scale.linear(range=[1,2])
        self.assertEqual(s(0.5), 1.5)

    def test_3(self):
        """
        linear(x) ignores extra range values if the domain is smaller than the range
        """
        s = scale.linear(domain=[-10,0], range=["red", "white", "green"], clamp=True)
        self.assertEqual(s(-5), "#ff8080")
        self.assertEqual(s(50), "#ffffff")

    def test_4(self):
        """
        linear(x) ignores extra domain values if the range is smaller than the domain
        """
        s = scale.linear(domain=[-10,0,100], range=["red", "white"], clamp=True)
        self.assertEqual(s(-5), "#ff8080")
        self.assertEqual(s(50), "#ffffff")

    def test_5(self):
        """
        linear(x) maps an empty domain to the range start
        """
        s = scale.linear(domain=[0,0], range=[1,2])
        self.assertEqual(s(0), 1)
        
        s = scale.linear(domain=[0,0], range=[2,1])
        self.assertEqual(s(1), 2)
    
    def test_6(self):
        """
        linear(x) can map a bilinear domain with two values to the corresponding
        range
        """
        s = scale.linear(domain=[1, 2])
        self.assertEqual(s.domain, [1,2])
        self.assertEqual(s(0.5), -0.5)
        self.assertEqual(s(1.0),  0.0)
        self.assertEqual(s(1.5),  0.5)
        self.assertEqual(s(2.0),  1.0)
        self.assertEqual(s(2.5),  1.5)
        self.assertEqual(s.invert(-0.5), 0.5)
        self.assertEqual(s.invert( 0.0), 1.0)
        self.assertEqual(s.invert( 0.5), 1.5)
        self.assertEqual(s.invert( 1.0), 2.0)
        self.assertEqual(s.invert( 1.5), 2.5)

    def test_7(self):
        """
        linear(x) can map a polylinear domain with more than two values to the
        corresponding range
        """
        s = scale.linear(domain=[-10, 0, 100], range=["red", "white", "green"])
        self.assertEqual(s.domain, [-10, 0, 100])
        self.assertEqual(s(-5), "#ff8080")
        self.assertEqual(s(50), "#80c080")
        self.assertEqual(s(75), "#40a040")
  
        s = scale.linear(domain=[4, 2, 1], range=[1, 2, 4])
        self.assertEqual(s(1.5), 3)
        self.assertEqual(s(3), 1.5)
        self.assertEqual(s.invert(1.5), 3)
        self.assertEqual(s.invert(3), 1.5)
        
        s = scale.linear(domain=[1, 2, 4],range=[4, 2, 1])
        self.assertEqual(s(1.5), 3)
        self.assertEqual(s(3), 1.5)
        self.assertEqual(s.invert(1.5), 3)
        self.assertEqual(s.invert(3), 1.5)

    def test_8(self):
        """
        linear.invert(y) maps a range value y to a domain value x
        """
        s = scale.linear(range=[1,2])
        self.assertEqual(s.invert(1.5), .5)

    def test_9(self):
        """
        linear.invert(y) maps an empty range to the domain start
        """
        s = scale.linear(domain=[1,2], range=[0,0])
        self.assertEqual(s.invert(0), 1)
        s = scale.linear(domain=[2,1], range=[0,0])
        self.assertEqual(s.invert(1), 2)

    def test_10(self):
        """
        linear.invert(y) coerces range values to numbers
        """
        s = scale.linear(range=["0", "2"])
        self.assertEqual(s.invert(1), .5)

        s = scale.linear(range=[np.datetime64("1990-01-01"), np.datetime64("1991-01-01")])
        self.assertEqual(s(.5), np.datetime64("1990-07-02"))

    def test_11(self):
        """
        linear.invert(y) returns None if the range is not coercible to number
        """
        s = scale.linear(range=["#000", "#fff"])
        self.assertEqual(s.invert("#999"), None)
        s = scale.linear(range=[0, "#fff"])
        self.assertEqual(s.invert("#999"), None)

    def test_12(self):
        """
        linear.domain(domain) accepts an array of numbers
        """
        self.assertEqual( scale.linear(domain=[]).domain, [])
        self.assertEqual( scale.linear(domain=[1,0]).domain, [1,0])
        self.assertEqual( scale.linear(domain=[1,2,3]).domain, [1,2,3])

    def test_16(self):
        """
        linear.range(range) does not coerce range to numbers
        """
        s = scale.linear(range=["0px", "2px"])
        self.assertEqual(s.range, ["0px", "2px"])
        self.assertEqual(s(.5), "1px")

    def test_17(self):
        """
        linear.range(range) can accept range values as colors
        """
        s = scale.linear(range=["red", "blue"])
        self.assertEqual(s(.5), "#800080")

        s = scale.linear(range=["#ff0000", "#0000ff"])
        self.assertEqual(s(.5), "#800080")

        s = scale.linear(range=["#f00", "#00f"])
        self.assertEqual(s(.5), "#800080")

    def test_18(self):
        """
        linear.range(range) can accept range values as arrays or objects
        """
        s = scale.linear(range=[{"color": "red"}, {"color": "blue"}])
        self.assertEqual(s(.5), {"color":"#800080"})

        s = scale.linear(range=[["red"], ["blue"]])
        self.assertEqual(s(.5), ["#800080"])

    def test_22(self):
        """
        linear.clamp() is false by default
        """
        self.assertEqual(scale.linear().clamp, False)
        self.assertEqual(scale.linear(range=[10, 20])(2), 30)
        self.assertEqual(scale.linear(range=[10, 20])(-1), 0)
        self.assertEqual(scale.linear(range=[10, 20]).invert(30), 2)
        self.assertEqual(scale.linear(range=[10, 20]).invert(0), -1)

    def test_23(self):
        """
        linear.clamp(true) restricts output values to the range
        """
        self.assertEqual(scale.linear(range=[10, 20],clamp=True)(2), 20)
        self.assertEqual(scale.linear(range=[10, 20],clamp=True)(-1), 10)

    def test_24(self):
        """
        linear.clamp(true) restricts input values to the domain
        """
        self.assertEqual(scale.linear(range=[10, 20],clamp=True).invert(30), 1)
        self.assertEqual(scale.linear(range=[10, 20],clamp=True).invert(0), 0)

    def test_25(self):
        """
        linear.clamp(clamp) coerces the specified clamp value to a boolean
        """
        self.assertEqual(scale.linear(clamp=True).clamp, True)
        self.assertEqual(scale.linear(clamp=1).clamp, True)
        self.assertEqual(scale.linear(clamp="").clamp, False)
        self.assertEqual(scale.linear(clamp=0).clamp, False)

    def test_26(self):
        """
        linear.interpolate(interpolate) takes a custom interpolator factory
        """
        pass

    def test_27(self):
        """
        linear.nice() is an alias for linear.nice(10)
        """
        self.assertEqual(scale.linear(domain=[0,.96]).nice().domain, [0, 1])
        self.assertEqual(scale.linear(domain=[0,96]).nice().domain, [0, 100])

    def test_28(self):
        """
        linear.nice(count) extends the domain to match the desired ticks
        """
        self.assertEqual(scale.linear(domain=[ 0,.96]).nice().domain, [0, 1])
        self.assertEqual(scale.linear(domain=[ 0, 96]).nice().domain, [0, 100])
        self.assertEqual(scale.linear(domain=[.96, 0]).nice().domain, [1, 0])
        self.assertEqual(scale.linear(domain=[ 96, 0]).nice().domain, [100, 0])
        self.assertEqual(scale.linear(domain=[0,-.96]).nice().domain, [0, -1])
        self.assertEqual(scale.linear(domain=[0, -96]).nice().domain, [0, -100])
        self.assertEqual(scale.linear(domain=[-.96,0]).nice().domain, [-1, 0])
        self.assertEqual(scale.linear(domain=[-96,0]).nice().domain, [-100, 0])
        self.assertEqual(scale.linear(domain=[-0.1,51.1]).nice(8).domain, [-10, 60])

    def test_29(self):
        """
        linear.nice(count) nices the domain, extending it to round numbers
        """
        self.assertEqual(scale.linear(domain=[1.1,10.9]).nice(10).domain, [1, 11])
        self.assertEqual(scale.linear(domain=[10.9,1.1]).nice(10).domain, [11, 1])
        self.assertEqual(scale.linear(domain=[.7,11.001]).nice(10).domain, [0, 12])
        self.assertEqual(scale.linear(domain=[123.1,6.7]).nice(10).domain, [130, 0])
        self.assertEqual(scale.linear(domain=[0,.49]).nice(10).domain, [0, .5])

    def test_30(self):
        """
        linear.nice(count) has no effect on degenerate domains
        """
        self.assertEqual(scale.linear(domain=[0,0]).nice(10).domain, [0, 0])
        self.assertEqual(scale.linear(domain=[.5,.5]).nice(10).domain, [.5, .5])

    def test_31(self):
        """
        linear.nice(count) nicing a polylinear domain only affects the extent
        """
        self.assertEqual(scale.linear(domain=[1.1, 1, 2, 3, 10.9]).nice(10).domain,
                         [1, 1, 2, 3, 11])
        self.assertEqual(scale.linear(domain=[123.1, 1, 2, 3, -.9]).nice(10).domain,
                         [130, 1, 2, 3, -10])

    def test_32(self):
        """
        linear.nice(count) accepts a tick count to control nicing step
        """
        self.assertEqual(scale.linear(domain=[12,87]).nice(5).domain,[0, 100])
        self.assertEqual(scale.linear(domain=[12,87]).nice(10).domain,[10, 90])
        self.assertEqual(scale.linear(domain=[12,87]).nice(100).domain,[12, 87])
        
if __name__ == "__main__":
    unittest.main()
