# pyd3.interpolate

pyd3.interpolate is a python translation of of the
[D3-interpolate](https://github.com/d3/d3-interpolate) module.


This module provides a variety of interpolation methods for blending between
two values. Values may be numbers, colors, strings, arrays, or even
deeply-nested objects. For example:

```python
i = pyd3.interpolate.number(10, 20)
i(0.0) # 10
i(0.2) # 12
i(0.5) # 15
i(1.0) # 20
```

The returned function `i` is called an *interpolator*. Given a starting value
*a* and an ending value *b*, it takes a parameter *t* in the domain [0, 1] and
returns the corresponding interpolated value between *a* and *b*. An
interpolator typically returns a value equivalent to *a* at *t* = 0 and a value
equivalent to *b* at *t* = 1.

You can interpolate more than just numbers. To find the perceptual midpoint
between steelblue and brown:

```python
pyd3.interpolate.rgb("steelblue", "brown")(0.5); # "#8e5c6d"
```

Here’s a more elaborate example demonstrating type inference used by
[value](#value):

```python
i = pyd3.interpolate.value({colors: ["red", "blue"]}, {colors: ["white", "black"]})
i(0.0) # {colors: ["#ff0000", "#0000ff"]}
i(0.5) # {colors: ["#ff8080", "#000080"]}
i(1.0) # {colors: ["#ffffff", "#000000"]}
```

Note that the generic value interpolator detects not only nested objects and
arrays, but also color strings and numbers embedded in strings!

## API Reference

<a name="value" href="#value">#</a> pyd3.interpolate.<b>value</b>(<i>a</i>, <i>b</i>)

Returns an interpolator between the two arbitrary values *a* and *b*. The
interpolator implementation is based on the type of the end value *b*, using
the following algorithm:

1. If *b* is a [color](#color), [rgb](#rgb) is used.
2. If *b* is a string, [string](#string) is used.
3. If *b* is an array, [array](#array) is used.
4. If *b* is a dict, [dict](#dict) is used.
5. Otherwise, [number](#number) is used.


Based on the chosen interpolator, *a* is coerced to a suitable corresponding
type. The behavior of this method may be augmented to support additional types
by pushing custom interpolator factories onto the [values](#values) array.

<a name="number" href="#number">#</a> pyd3.interpolate.<b>number</b>(<i>a</i>, <i>b</i>)

Returns an interpolator between the two numbers *a* and *b*. The returned
interpolator is equivalent to:

```python
def interpolate(t):
  return a * (1 - t) + b * t
```

Caution: avoid interpolating to or from the number zero when the interpolator
is used to generate a string. When very small values are stringified, they may
be converted to scientific notation, which is an invalid attribute or style
property value. For example, the number `0.0000001` is converted to the string
`"1e-7"`. This is particularly noticeable with interpolating opacity. To avoid
scientific notation, start or end the transition at 1e-6: the smallest value
that is not stringified in scientific notation.

<a name="round" href="#round">#</a> pyd3.interpolate.<b>round</b>(<i>a</i>, <i>b</i>)

Returns an interpolator between the two numbers *a* and *b*; the interpolator
is similar to [number](#number), except it will round the resulting value to
the nearest integer.

<a name="string" href="#string">#</a> pyd3.interpolate.<b>string</b>(<i>a</i>, <i>b</i>)

Returns an interpolator between the two strings *a* and *b*. The string
interpolator finds numbers embedded in *a* and *b*, where each number is of the
form understood by Python. A few examples of numbers that will be detected
within a string: `-1`, `42`, `3.14159`, and `6.0221413e+23`.

For each number embedded in *b*, the interpolator will attempt to find a
corresponding number in *a*. If a corresponding number is found, a numeric
interpolator is created using [number](#number). The remaining parts of the
string *b* are used as a template: the static parts of the string *b* remain
constant for the interpolation, with the interpolated numeric values embedded
in the template.

For example, if *a* is `"300 12px sans-serif"`, and *b* is `"500 36px
Comic-Sans"`, two embedded numbers are found. The remaining static parts of the
string are a space between the two numbers (`" "`), and the suffix (`"px
Comic-Sans"`). The result of the interpolator at *t* = .5 is `"400 24px
Comic-Sans"`.

<a name="list" href="#list">#</a> pyd3.interpolate.<b>list</b>(<i>a</i>, <i>b</i>)

Returns an interpolator between the two lists *a* and *b*. Internally, a list
template is created that is the same length in *b*. For each element in *b*, if
there exists a corresponding element in *a*, a generic interpolator is created
for the two elements using [value](#value). If there is no such element, the
static value from *b* is used in the template. Then, for the given parameter
*t*, the template’s embedded interpolators are evaluated. The updated list
template is then returned.

For example, if *a* is the list `[0, 1]` and *b* is the list `[1, 10, 100]`,
then the result of the interpolator for *t* = .5 is the list `[.5, 5.5, 100]`.


<a name="dict" href="#dict">#</a> pyd3.interpolate.<b>dict</b>(<i>a</i>, <i>b</i>)

Returns an interpolator between the two dicts *a* and *b*. Internally, a dict
template is created that has the same properties as *b*. For each property in
*b*, if there exists a corresponding property in *a*, a generic interpolator is
created for the two elements using [value](#value). If there is no such
property, the static value from *b* is used in the template. Then, for the
given parameter *t*, the template's embedded interpolators are evaluated and
the updated object template is then returned.

For example, if *a* is the dict `{"x": 0, "y": 1}` and *b* is the dict `{"x":
1, "y": 10, "z": 100}`, the result of the interpolator for *t* = .5 is the dict
`{"x": .5, "y": 5.5, "z": 100}`.

dict interpolation is particularly useful for *dataspace interpolation*, where
data is interpolated rather than attribute values.

<a name="rgb" href="#rgb">#</a> pyd3.interpolate.<b>rgb</b>(<i>a</i>, <i>b</i>)

<img src="https://raw.githubusercontent.com/d3/d3-interpolate/master/img/rgb.png" width="100%" height="40" alt="rgb">

Returns an RGB color space interpolator between the two colors *a* and *b*. The
colors *a* and *b* need not be in RGB; they will be converted to RGB using
[color.rgb](https://github.com/d3/d3-color#rgb). The return value of the
interpolator is a hexadecimal RGB string.

