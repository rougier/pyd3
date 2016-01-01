pyd3 is a python translation of some modules of the [D3](https://github.com/d3)
library.

**Content**

  * [color]()   — Color spaces! RGB, HSL, Cubehelix, Lab (CIELAB) and HCL (CIELCH).
  * [interpolate](#interpolate) — Interpolate numbers, colors, strings, arrays, objects, whatever!


<a name="interpolate" href="#interpolate">#</a>interpolate

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
