# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
"""
This is a python translation of the `d3-interpolate
<https://github.com/d3/d3-interpolate>`_ javascript module.

This module provides a variety of interpolation methods for blending between
two values. Values may be numbers, colors, strings, arrays, or even
deeply-nested objects. For example::

   i = interpolate.number(10, 20)
   i(0.0) # 10
   i(0.2) # 12
   i(0.5) # 15
   i(1.0) # 20

The returned function `i` is called an *interpolator*. Given a starting value
*a* and an ending value *b*, it takes a parameter *t* in the domain [0, 1] and
returns the corresponding interpolated value between *a* and *b*. An
interpolator typically returns a value equivalent to *a* at *t* = 0 and a value
equivalent to *b* at *t* = 1.

You can interpolate more than just numbers. To find the perceptual midpoint
between steelblue and brown::

  interpolate.rgb("white", "black")(0.5) # "#808080

Here’s a more elaborate example demonstrating type inference used by value::

  i = interpolate.value({"colors": ["red", "blue"]},
                        {"colors": ["white", "black"]});
  i(0.0); # {'colors': ["#ff0000", "#0000ff"]}
  i(0.5); # {'colors': ["#ff8080", "#000080"]}
  i(1.0); # {'colors': ["#ffffff", "#000000"]}

Note that the generic value interpolator detects not only nested objects and
lists, but also color strings and numbers embedded in strings!
"""
import re
from pyd3.color import Color

# We saved python core objects here because we'll override some of them (see
# end of file)
py_list  = list
py_dict  = dict
py_tuple = tuple
py_round = round


def interpolate_value(a,b):
    """
    Returns an interpolator between the two arbitrary values *a* and *b*. The
    interpolator implementation is based on the type of the end value *b*,
    using the following algorithm:

    1. If *b* is a color, [rgb](#rgb) is used.
    2. If *b* is a string, [string](#string) is used.
    3. If *b* is a list, [list](#list) is used.
    4. If *b* is a dict, [dict](#dict) is used.
    5. Otherwise, [number](#number) is used.

    Based on the chosen interpolator, *a* is coerced to a suitable
    corresponding type. The behavior of this method may be augmented to support
    additional types by pushing custom interpolator factories onto the values
    array.
    """
    
    if isinstance(b, str):
        try:
            a, b = Color(a), Color(b)
        except ValueError:
            try:
                a, b = float(a), float(b)
            except ValueError:
                return interpolate_string(a,b)
            else:
                return interpolate_number(float(a),float(b))
        else:
            return interpolate_rgb(Color(a),Color(b))                
    elif isinstance(b, (py_list,py_tuple)):
        return interpolate_list(a,b)
    elif isinstance(b, py_dict):
        return interpolate_dict(a,b)
    else:
        return interpolate_number(a,b)


def interpolate_number(a, b):
    """
    Returns an interpolator between the two numbers *a* and *b*. The returned
    interpolator is equivalent to::

    def interpolate(t):
        return a * (1 - t) + b * t

    Caution: avoid interpolating to or from the number zero when the
    interpolator is used to generate a string. When very small values are
    stringified, they may be converted to scientific notation, which is an
    invalid attribute or style property value. For example, the number
    `0.0000001` is converted to the string `"1e-7"`. This is particularly
    noticeable with interpolating opacity. To avoid scientific notation, start
    or end the transition at 1e-6: the smallest value that is not stringified
    in scientific notation.
    """
    
    b = b - a
    def _interpolate(t):
        return a + t * b
    return _interpolate


def interpolate_round(a, b):
    """
    Returns an interpolator between the two numbers *a* and *b*; the
    interpolator is similar to number, except it will round the resulting value
    to the nearest integer.
    """
    
    b = b - a
    def _interpolate(t):
        return int(py_round(a + b * t))
    return _interpolate


def interpolate_rgb(a, b):
    """
    Returns an RGB color space interpolator between the two colors a and b. The
    colors a and b need not be in RGB; they will be converted to RGB using
    color.rgb. The return value of the interpolator is a hexadecimal RGB
    string.
    """
    
    a, b = Color(a), Color(b)
    ar, ag, ab = a.rgb
    br, bg, bb = b.rgb
    br, bg, bb = br-ar, bg-ag, bb-ab
    def _interpolate(t):
        return Color(rgb=(ar + t*br, ag + t*bg, ab + t*bb))
    return _interpolate


def interpolate_string(a, b):
    """
    Returns an interpolator between the two strings *a* and *b*. The string
    interpolator finds numbers embedded in *a* and *b*, where each number is of
    the form understood by JavaScript. A few examples of numbers that will be
    detected within a string: `-1`, `42`, `3.14159`, and `6.0221413e+23`.

    For each number embedded in *b*, the interpolator will attempt to find a
    corresponding number in *a*. If a corresponding number is found, a numeric
    interpolator is created using [number](#number). The remaining parts of the
    string *b* are used as a template: the static parts of the string *b*
    remain constant for the interpolation, with the interpolated numeric values
    embedded in the template.

    For example, if *a* is `"300 12px sans-serif"`, and *b* is `"500 36px
    Comic-Sans"`, two embedded numbers are found. The remaining static parts of
    the string are a space between the two numbers (`" "`), and the suffix
    (`"px Comic-Sans"`). The result of the interpolator at *t* = .5 is `"400
    24px Comic-Sans"`.
    """
    
    # Regular expression matching any number in decimal notation
    number = "[+-]?((\d+\.\d*)|(\d*\.\d+)|(([1-9][0-9]*)|0+))(([eE][-+]?\d+)?)"

    # Get all values from string a
    a_values = []
    for match in re.finditer(number, a):
        a_values.append(eval(match.group(0)))

    # Get as many values from string b and replace them with "%g"
    b_values = []
    def replace(match):
        if len(b_values) < len(a_values):
            b_values.append(eval(match.group(0)))
            return "%g"
        else:
            return match.group(0)
    text = re.sub(number, replace, b)

    # Build individual interpolators
    interpolators = [interpolate_number(a_values[i],b_values[i])
                                       for i in range(len(b_values))]
    def _interpolate(t):
        return text % tuple([interpolator(t) for interpolator in interpolators])
    return _interpolate


def interpolate_list(a, b):
    """
    Returns an interpolator between the two lists *a* and *b*. Internally, a
    list template is created that is the same length in *b*. For each element
    in *b*, if there exists a corresponding element in *a*, a generic
    interpolator is created for the two elements using [value](#value). If
    there is no such element, the static value from *b* is used in the
    template. Then, for the given parameter *t*, the template’s embedded
    interpolators are evaluated. The updated list template is then returned.

    For example, if *a* is the list `[0, 1]` and *b* is the list `[1, 10,
    100]`, then the result of the interpolator for *t* = .5 is the list `[.5,
    5.5, 100]`.
    """
    
    _interpolators = []
    for i in range(len(b)):
        if i < len(a):
            _interpolators.append(interpolate_value(a[i],b[i]))
        else:
            _interpolators.append(lambda t: b[i])

    def _interpolate(t):
        return [f(t) for f in _interpolators]
    return _interpolate


def interpolate_dict(a, b):
    """
    Returns an interpolator between the two dicts *a* and *b*. Internally, a
    dict template is created that has the same properties as *b*. For each
    property in *b*, if there exists a corresponding property in *a*, a generic
    interpolator is created for the two elements using [value](#value). If
    there is no such property, the static value from *b* is used in the
    template. Then, for the given parameter *t*, the template's embedded
    interpolators are evaluated and the updated object template is then
    returned.

    For example, if *a* is the dict `{"x": 0, "y": 1}` and *b* is the dict
    `{"x": 1, "y": 10, "z": 100}`, the result of the interpolator for *t* = .5
    is the dict `{"x": .5, "y": 5.5, "z": 100}`.

    dict interpolation is particularly useful for *dataspace interpolation*,
    where data is interpolated rather than attribute values.
    """
    
    _interpolators = {}

    # Values present in a but not in b (not interpolated)
    for key in a.keys():
        if key not in b.keys():
            _interpolators[key] = lambda t, k=key: a[k]

    # Values present in a but not in b (not interpolated)
    for key in b.keys():
        if key not in a.keys():
            _interpolators[key] = lambda t, k=key: b[k]
        else:
            _interpolators[key] = interpolate_value(a[key],b[key])
        
    def _interpolate(t):
        return {key:f(t) for (key,f) in _interpolators.items()}
    return _interpolate


# Shortcuts to allow convenient notation such as interpolate.string(a,b)
rgb    = interpolate_rgb
list   = interpolate_list
dict   = interpolate_dict
value  = interpolate_value
number = interpolate_number
round  = interpolate_round
string = interpolate_string

# We don't want to allow to import everything since it would overrides list,
# dict and round
__all__ = [ interpolate_rgb,   interpolate_list,   interpolate_dict,
            interpolate_value, interpolate_number, interpolate_round,
            interpolate_string ]

