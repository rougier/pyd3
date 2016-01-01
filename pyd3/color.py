# -----------------------------------------------------------------------------
# Copyright (c) 2016, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
import re
import colorsys

__colors__ = {
    "aliceblue":            "#f0f8ff",
    "antiquewhite":         "#faebd7",
    "aqua":                 "#00ffff",
    "aquamarine":           "#7fffd4",
    "azure":                "#f0ffff",
    "beige":                "#f5f5dc",
    "bisque":               "#ffe4c4",
    "black":                "#000000",
    "blanchedalmond":       "#ffebcd",
    "blue":                 "#0000ff",
    "blueviolet":           "#8a2be2",
    "brown":                "#a52a2a",
    "burlywood":            "#deb887",
    "cadetblue":            "#5f9ea0",
    "chartreuse":           "#7fff00",
    "chocolate":            "#d2691e",
    "coral":                "#ff7f50",
    "cornflowerblue":       "#6495ed",
    "cornsilk":             "#fff8dc",
    "crimson":              "#dc143c",
    "cyan":                 "#00ffff",
    "darkblue":             "#00008b",
    "darkcyan":             "#008b8b",
    "darkgoldenrod":        "#b8860b",
    "darkgray":             "#a9a9a9",
    "darkgrey":             "#a9a9a9",
    "darkgreen":            "#006400",
    "darkkhaki":            "#bdb76b",
    "darkmagenta":          "#8b008b",
    "darkolivegreen":       "#556b2f",
    "darkorange":           "#ff8c00",
    "darkorchid":           "#9932cc",
    "darkred":              "#8b0000",
    "darksalmon":           "#e9967a",
    "darkseagreen":         "#8fbc8f",
    "darkslateblue":        "#483d8b",
    "darkslategray":        "#2f4f4f",
    "darkslategrey":        "#2f4f4f",
    "darkturquoise":        "#00ced1",
    "darkviolet":           "#9400d3",
    "deeppink":             "#ff1493",
    "deepskyblue":          "#00bfff",
    "dimgray":              "#696969",
    "dimgrey":              "#696969",
    "dodgerblue":           "#1e90ff",
    "firebrick":            "#b22222",
    "floralwhite":          "#fffaf0",
    "forestgreen":          "#228b22",
    "fuchsia":              "#ff00ff",
    "gainsboro":            "#dcdcdc",
    "ghostwhite":           "#f8f8ff",
    "gold":                 "#ffd700",
    "goldenrod":            "#daa520",
    "gray":                 "#808080",
    "grey":                 "#808080",
    "green":                "#008000",
    "greenyellow":          "#adff2f",
    "honeydew":             "#f0fff0",
    "hotpink":              "#ff69b4",
    "indianred":            "#cd5c5c",
    "indigo":               "#4b0082",
    "ivory":                "#fffff0",
    "khaki":                "#f0e68c",
    "lavender":             "#e6e6fa",
    "lavenderblush":        "#fff0f5",
    "lawngreen":            "#7cfc00",
    "lemonchiffon":         "#fffacd",
    "lightblue":            "#add8e6",
    "lightcoral":           "#f08080",
    "lightcyan":            "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray":            "#d3d3d3",
    "lightgrey":            "#d3d3d3",
    "lightgreen":           "#90ee90",
    "lightpink":            "#ffb6c1",
    "lightsalmon":          "#ffa07a",
    "lightseagreen":        "#20b2aa",
    "lightskyblue":         "#87cefa",
    "lightslategray":       "#778899",
    "lightslategrey":       "#778899",
    "lightsteelblue":       "#b0c4de",
    "lightyellow":          "#ffffe0",
    "lime":                 "#00ff00",
    "limegreen":            "#32cd32",
    "linen":                "#faf0e6",
    "magenta":              "#ff00ff",
    "maroon":               "#800000",
    "mediumaquamarine":     "#66cdaa",
    "mediumblue":           "#0000cd",
    "mediumorchid":         "#ba55d3",
    "mediumpurple":         "#9370d8",
    "mediumseagreen":       "#3cb371",
    "mediumslateblue":      "#7b68ee",
    "mediumspringgreen":    "#00fa9a",
    "mediumturquoise":      "#48d1cc",
    "mediumvioletred":      "#c71585",
    "midnightblue":         "#191970",
    "mintcream":            "#f5fffa",
    "mistyrose":            "#ffe4e1",
    "moccasin":             "#ffe4b5",
    "navajowhite":          "#ffdead",
    "navy":                 "#000080",
    "oldlace":              "#fdf5e6",
    "olive":                "#808000",
    "olivedrab":            "#6b8e23",
    "orange":               "#ffa500",
    "orangered":            "#ff4500",
    "orchid":               "#da70d6",
    "palegoldenrod":        "#eee8aa",
    "palegreen":            "#98fb98",
    "paleturquoise":        "#afeeee",
    "palevioletred":        "#d87093",
    "papayawhip":           "#ffefd5",
    "peachpuff":            "#ffdab9",
    "peru":                 "#cd853f",
    "pink":                 "#ffc0cb",
    "plum":                 "#dda0dd",
    "powderblue":           "#b0e0e6",
    "purple":               "#800080",
    "red":                  "#ff0000",
    "rosybrown":            "#bc8f8f",
    "royalblue":            "#4169e1",
    "saddlebrown":          "#8b4513",
    "salmon":               "#fa8072",
    "sandybrown":           "#f4a460",
    "seagreen":             "#2e8b57",
    "seashell":             "#fff5ee",
    "sienna":               "#a0522d",
    "silver":               "#c0c0c0",
    "skyblue":              "#87ceeb",
    "slateblue":            "#6a5acd",
    "slategray":            "#708090",
    "slategrey":            "#708090",
    "snow":                 "#fffafa",
    "springgreen":          "#00ff7f",
    "steelblue":            "#4682b4",
    "tan":                  "#d2b48c",
    "teal":                 "#008080",
    "thistle":              "#d8bfd8",
    "tomato":               "#ff6347",
    "turquoise":            "#40e0d0",
    "violet":               "#ee82ee",
    "wheat":                "#f5deb3",
    "white":                "#ffffff",
    "whitesmoke":           "#f5f5f5",
    "yellow":               "#ffff00",
    "yellowgreen":          "#9acd32"
}

def web2hex(color):
    if color in __colors__.keys():
        return __colors__[color]
    raise ValueError('Unknwon color string "%s"' % color)

def hex2rgb(color):

    hex_color= re.compile(
        "\A#[a-fA-F0-9]{6}\Z|\A#[a-fA-F0-9]{3}\Z|\A#[a-fA-F0-9]{1}\Z")
    if hex_color.match(color) is None:
        raise ValueError('Invalid hex color string "%s"' % color)

    color = color.lstrip('#')
    n = len(color)
    # 1 single byte component (#x)
    if n == 1:
        v = int(color,16)*17/255.0
        return v,v,v
    # 3 single byte components (#xyz)
    if n == 3:
        return tuple( (int(color[i:i+1], 16)*17)/255.0 for i in range(0,3))
    # 3 double byte components (#xxyyzz)
    return tuple(int(color[i:i+n//3], 16)/255.0 for i in range(0,n,n//3))

def rgb2hex(r,g,b):
    return '#' + ''.join(["%02x" % int(round(v*255)) for v in (r,g,b)])
    
def rgb2hsl(r,g,b):
    h,l,s = colorsys.rgb_to_hls(r,g,b)
    return h,s,l

def hsl2rgb(h,s,l):
    return colorsys.hls_to_rgb(h,l,s)

def rgb2hsv(r,g,b):
    return colorsys.rgb_to_hsv(r,g,b)

def hsv2rgb(h,s,v):
    return colorsys.hsv_to_rgb(r,g,b)

def rgb2hsl(r,g,b):
    h,l,s = colorsys.rgb_to_hls(r,g,b)
    return h,s,l

hsl2hex = lambda x: rgb2hex(hsl2rgb(x))
hex2hsl = lambda x: rgb2hsl(hex2rgb(x))
rgb2web = lambda x: hex2web(rgb2hex(x))
web2rgb = lambda x: hex2rgb(web2hex(x))
web2hsl = lambda x: rgb2hsl(web2rgb(x))
hsl2web = lambda x: rgb2web(hsl2rgb(x))


class Color(object):
    """
    color = Color(RGB=(255, 255, 255))
    color = Color(rgb=(1.0, 1.0, 1.0))
    color = Color("#ffffff")
    color = Color("#fff")
    color = Color("white")
    color = Color(Color("white"))
    """
    
    def __init__(self, color=None, *args, **kwargs):
        if color is not None:
            if isinstance(color, str):
                if color[0] == '#':
                    r,g,b = hex2rgb(color)
                else:
                    r,g,b = web2rgb(color)
                self.rgb = r,g,b
                self.alpha = 1.0
            elif isinstance(color, Color):
                self.rgb = color.rgb
                self.alpha = color.alpha
            else:
                raise ValueError('Color argument not understood "%s"' % repr(color))
        elif "rgb" in kwargs.keys():
            self.rgb = kwargs["rgb"]
            self.alpha=  1.0
        elif "rgba" in kwargs.keys():
            r,g,b,a = kwargs["rgb"]
            self.rgb = rgb
            self.alpha = a
        elif "RGB" in kwargs.keys():
            R,G,B = kwargs["RGB"]
            self.rgb = R/255.0, G/255.0, B/255.0
            self.alpha = 1.0
        elif "RGBA" in kwargs.keys():
            R,G,B,A = kwargs["RGB"]
            self.rgb = R/255.0, G/255.0, B/255.0
            self.alpha = A/255.0
        else:
            self.rgb = 1.0, 1.0, 1.0
            self.alpha= 1.0

    def __eq__(self,other):
        if isinstance(other,Color):
            return rgb2hex(*self.rgb) == rgb2hex(*other.rgb)
        elif isinstance(other,str):
            return rgb2hex(*self.rgb) == other
        elif isinstance(other,tuple):
            return self.rgb == other
        else:
            return False
            
    def __repr__(self):
        return rgb2hex(*self.rgb)

__all__ = [Color]
