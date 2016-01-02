# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
"""
This is a python translation of the `d3-scale
<https://github.com/d3/d3-scale>`_ javascript module.

Scales are a convenient abstraction for a fundamental task in
visualization: mapping a dimension of abstract data to a visual
representation. Although most often used for position-encoding quantitative
data, such as mapping a measurement in meters to a position in pixels for dots
in a scatterplot, scales can represent virtually any visual encoding, such as
diverging colors, stroke widths, or symbol size. Scales can also be used with
virtually any type of data, such as named categorical data or discrete data
that requires sensible breaks.

For continuous quantitative data, you typically want a linear scale. (For time
series data, a time scale.) If the distribution calls for it, consider
transforming data using a power or log scale. A quantize scale may aid
differentiation by rounding continuous data to a fixed set of discrete values;
similarly, a quantile scale computes quantiles from a sample population, and a
threshold scale allows you to specify arbitrary breaks in continuous
data. Several built-in sequential color scales are also provided. (If you don’t
like these palettes, try ColorBrewer.)

For discrete ordinal (ordered) or categorical (unordered) data, an ordinal
scale specifies an explicit mapping from a set of data values to a
corresponding set of visual attributes (such as colors). The related band and
point scales are useful for position-encoding ordinal data, such as bars in a
bar chart or dots in an categorical scatterplot. Several built-in categorical
color scales are also provided.

Scales have no intrinsic visual representation. However, most scales can
generate and format ticks for reference marks to aid in the construction of
axes.
"""

import numpy as np
from pyd3 import interpolate

py_range = range

def interpolate_number(x, xp, yp, clamp=True):
    """
    Specialized interpolation for array of scalars
    """
    x = np.asarray(x)
    
    # Specific case for empty domain
    if xp[0] == xp[-1] or len(xp)<2:
        if len(x.shape) == 0:
            return yp[0]
        else:
            return [yp[0],]*len(x)

    # Extrapolate
    if not clamp:
        # Single value
        if len(x.shape) == 0:
            if   x < xp[0]:
                return yp[ 0] + (x-xp[ 0])*(yp[ 0]-yp[ 1]) / (xp[ 0]-xp[ 1])
            elif x > xp[-1]:
                return yp[-1] + (x-xp[-1])*(yp[-1]-yp[-2]) / (xp[-1]-xp[-2])
            else:
                return np.interp(x, xp, yp)
        # Values list
        else:
            # Specific case for empty domain
            if xp[0] == xp[-1] or len(xp)<2:
                return [yp[0],]*len(x)
            y = np.interp(x, xp, yp)
            y[x < xp[ 0]] = yp[ 0] + (x[x<xp[ 0]]-xp[ 0]) * (yp[ 0]-yp[ 1]) / (xp[ 0]-xp[ 1])
            y[x > xp[-1]] = yp[-1] + (x[x>xp[-1]]-xp[-1]) * (yp[-1]-yp[-2]) / (xp[-1]-xp[-2])
            return y

    # Interpolate
    return np.interp(x, xp, yp)



def interpolate_time(x, xp, yp, clamp=True):
    """
    Specialized interpolation for array of datetime values
    """
    x = np.asarray(x)
    
    # Specific case for empty domain
    if xp[0] == xp[-1] or len(xp)<2:
        if len(x.shape) == 0:
            return yp[0]
        else:
            return [yp[0],]*len(x)

    delta = np.cumsum(yp[1:] - yp[:-1])
    delta = np.insert(delta, 0, 0)
    dtype = delta.dtype

    interpolated = np.array(interpolate_number(x, xp, delta.astype(int), clamp))
    return yp[0] + interpolated.astype(delta.dtype)


def interpolate_value(x, xp, yp, clamp=True):    
    """
    Generic interpolation
    """
    x = np.asarray(x)
    n = len(xp)
    
    # Specific case for empty domain
    if xp[0] == xp[-1] or len(xp)<2:
        if len(x.shape) == 0:
            return yp[0]
        else:
            return [yp[0],]*len(x)
    
    # Build (n-1) interpolators for each interval in yp
    interpolators = []
    for i in range(len(yp)-1):
        interpolators.append(interpolate.value(yp[i],yp[i+1]))

    # Find corresponding interpolator foreach x value
    xi = np.searchsorted(xp,x)
    
    # Single value
    if len(x.shape) == 0:
        # Find indices of x within xp
        if xi == 0:
            xi = 1   # index 0 (= prepend) is invalid
        elif xi == n:
            xi = n-1 # index n (= append) is invalid
        xi -= 1

        # Normalized x values in each interval
        v = np.arange(len(xp))
        nx = interpolate_number(x, xp, np.arange(len(xp)), clamp=clamp) - xi
        return interpolators[xi](nx)
    
    # Values list
    else:
        # Find indices of x within xp
        xi[xi==0] = 1   # index 0 (= prepend) is invalid
        xi[xi==n] = n-1 # index n (= append) is invalid
        xi -= 1

        # Normalized x values in each interval
        v = np.arange(len(xp))
        nx = interpolate_number(x, xp, np.arange(len(xp)), clamp=clamp) - xi

        # Get output value for each x
        return [interpolators[i](x) for i,x in zip(xi,nx)]



class ContinuousScale(object):
    """
    Continuous scales map a continuous, quantitative input domain to a
    continuous output range. If the range is also numeric, the mapping may be
    inverted. A continuous scale is not constructed directly; instead, try a
    linear, power, log, identity, time or sequential color scale.

    # continuous(value)

    Given a value from the domain, returns the corresponding value from the
    range. If the given value is outside the domain, and clamping is not
    enabled, the mapping may be extrapolated such that the returned value is
    outside the range. For example, to apply a position encoding::

    x = scale.linear(domain=[10, 130], range=[0, 960])
    x(20) # 80
    x(50) # 320

    Or to apply a color encoding::

    color = scale.linear(domain=[10, 100], range=["brown", "steelblue"])
    color(20) # "#9a3439"
    color(50) # "#7b5167"
    """
    
    def __init__(self, domain=[0,1], range=[0,1], clamp=False, interpolate=None):

        self._update_domain_range(domain, range)
        self._clamp  = clamp
        if isinstance(range[0], (int,float)):
            self._interpolate = interpolate_number
        elif isinstance(range[0], np.datetime64):
            self._interpolate = interpolate_time
        else:
            self._interpolate = interpolate_value

    @property
    def clamp(self):
        return self._clamp

    @clamp.setter
    def clamp(self, clamp):
        self._clamp = clamp

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, domain):
        self.update_domain_range(domain, self._range)

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, range):
        self._update_domain_range(self._domain, range)


    def _update_domain_range(self, domain, range):

        # Store domain and range
        self._domain = domain
        self._range = range
        
        # Ensure len(domain) == len(range)
        n = min(len(self.domain), len(self.range))
        domain = domain[:n]
        range  = range[:n]

        # Coerce domain values if necessary
        # (domain may have been given as ["1", "2"])
        if not isinstance(domain, np.ndarray):
            try:
                domain = [float(v) for v in domain]
            except:
                pass

        # Forward domain & range
        # (domain must be sorted in increasing order)
        domain = np.asarray(domain)
        sorted = np.argsort(domain)
        self._forward_domain = domain[sorted]
        if isinstance(range, np.ndarray):
            self._forward_range = range[sorted]
        else:
            self._forward_range = [range[i] for i in sorted]

        # Try to convert range to a numpy array if possible
        if len(self._forward_range):
            if isinstance(self._forward_range[0], (int,float, np.datetime64)):
                self._forward_range = np.asarray(self._forward_range)
            
        # Inverse domain & range
        # (range must be sorted in increasing order)
        if not isinstance(range, np.ndarray):
            try:
                range = [float(v) for v in range]
            except:
                self._inverse_domain = None
                self._inverse_range = None
                return
        range = np.asarray(range)
        sorted = np.argsort(range)        
        self._inverse_range = range[sorted]
        self._inverse_domain = domain[sorted]
            


    
class LinearScale(ContinuousScale):
    def __init__(self, domain=[0,1], range=[0,1], clamp=False):
        ContinuousScale.__init__(self, domain, range, clamp)

    def __call__(self, values):
        return self._interpolate(values, self._forward_domain, self._forward_range, self._clamp)

    def invert(self, values):
        if self._inverse_range is not None:
            return self._interpolate(values, self._inverse_range, self._inverse_domain, self._clamp)
        else:
            return None


linear = LinearScale
    


# class QuantizeScale(object):
#     def __init__(self, domain=[0,1], range=[0,1], clamp=True):
#         self._domain = domain
#         self._range  = np.linspace(0,len(range)-1,num=len(domain))
#         self._values = list(range)
#         self._clamp  = clamp
#         self._interpolate = interpolate
        
#     def __call__(self, values):
#         indices = np.round(self._interpolate(values, self._domain, self._range))
#         return self._values[indices.astype(int)]

#     def invert(self, values):
#         values = np.asarray(values)
#         if len(values.shape) == 0:
#             index = self._values.index(values)
#             return self._interpolate(index, self._range, self._domain)
#         else:
#             indices = [self._values.index(value) for value in values]
#             return self._interpolate(indices, self._range, self._domain)


# x = QuantizeScale(domain=[10,100], range=[1,2,4])
# print(x(20))
# print(x(50))
# print(x(80))
# print(x.invert(4))
# print(x.invert([1,2,4]))

# x = LinearScale(domain=[0,100], range=[0,1])
# print(x.invert(x(np.linspace(0,100,11))))
#x = LinearScale(domain=[0,100], range=[Color("black"),Color("white")])
#print(x(100))
#print(x.invert(x(np.linspace(0,100,11))))

# def interpolate_time(x, xp, yp):
#     delta = np.cumsum(T[1:] - T[:-1])
#     delta = np.insert(delta, 0, 0)
#     dtype = delta.dtype
#     return yp[0] + np.interp(x, xp, delta.astype(int)).astype(delta.dtype)


# T = np.array(['2005-01-01T00:00', '2005-01-02T00:00', '2005-01-03T00:00'], dtype='datetime64')
# print(interpolate_time( [0], [0,1,2], T)[0])
# print(interpolate_time( [1], [0,1,2], T)[0])
# print(interpolate_time( [2], [0,1,2], T)[0])
# print(interpolate_time( [-1], [0,1,2], T, False)[0])

# print(interpolate( -1, [0,1], [0,1], clamp=True))
# print(interpolate( +2, [0,1], [0,1], clamp=True))
# print(interpolate( -1, [0,1], [0,1], clamp=False))
# print(interpolate( +2, [0,1], [0,1], clamp=False))


