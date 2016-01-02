pyd3 is a python translation of some modules of the [D3](https://github.com/d3)
library.

**Content**

  * [color]()   — Color spaces! RGB, HSL, Cubehelix, Lab (CIELAB) and HCL (CIELCH).
  * [interpolate](#interpolate) — Interpolate numbers, colors, strings, arrays, objects, whatever!
  * [scale](#scale) — Encodings that map abstract data to visual representation.
    * [continuous](#continuous) — map a continuous, quantitative input domain to a continuous output range.
  
<a name="interpolate" href="#interpolate">#</a><b>interpolate</b>

This module provides a variety of interpolation methods for blending between
two values. Values may be numbers, colors, strings, arrays, or even
deeply-nested objects. For example:

```python
i = interpolate.number(10, 20)
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
interpolate.rgb("white", "black")(0.5) # "#808080
```

Here’s a more elaborate example demonstrating type inference used by value:

```python
i = interpolate.value({"colors": ["red", "blue"]},
                      {"colors": ["white", "black"]})
i(0.0) # {'colors': ["#ff0000", "#0000ff"]}
i(0.5) # {'colors': ["#ff8080", "#000080"]}
i(1.0) # {'colors': ["#ffffff", "#000000"]}
```

Note that the generic value interpolator detects not only nested objects and
lists, but also color strings and numbers embedded in strings!


<a name="scale" href="#scale">#</a><b>scale</b>

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

<a name="continuous" href="#continuous">#</a><b>continuous</b>

Given a value from the domain, returns the corresponding value from the
range. If the given value is outside the domain, and clamping is not
enabled, the mapping may be extrapolated such that the returned value is
outside the range. For example, to apply a position encoding:

```python
x = scale.linear(domain=[10, 130], range=[0, 960])
x(20) # 80
x(50) # 320
```

Or to apply a color encoding:

```python
color = scale.linear(domain=[10, 100], range=["brown", "steelblue"])
color(20) # "#9a3439"
color(50) # "#7b5167"
```
