import matplotlib as mpl
import numpy as np


def interpolate_colors(color_start, color_end, n):
    if (type(color_start) == str) or (type(color_end) == str):
        if color_start in mpl.colors.cnames.keys():
            color_start = hex_to_rgb(mpl.colors.cnames[color_start])
        else:
            color_start = hex_to_rgb(color_start)
        if color_end in mpl.colors.cnames.keys():
            color_end = hex_to_rgb(mpl.colors.cnames[color_end])
        else:
            color_end = hex_to_rgb(color_end)
    print("color_start", color_start)
    print("color_end", color_end)

    colors = []
    for i in range(n):
        fraction = i / float(n - 1)
        colors.append(rgb_to_hex([
            int(color_start[j] + (color_end[j] - color_start[j]) * fraction)
            for j in range(3)
        ]))
    return colors


def rgb_to_hex(rgb):
    # Convert RGB colors to hexadecimal format
    return '0x{:02x}{:02x}{:02x}'.format(*rgb)


def hex_to_rgb(hex_in):
    # Convert Hexadecimal color to RGB format
    hex_in = hex_in.strip("#")
    return tuple(int(hex_in[i:i + 2], 16) for i in (0, 2, 4))


def trim_cmap(colormap, cmin=0.20, cmax=1.00):
    # Takes a Matplotlib Colormap and a min and max value
    # Returns trimmed version of that colormap to only the specified color space between 0.0 and 1.0
    cmap = mpl.colormaps[colormap]
    colors = cmap(np.linspace(cmin, cmax, cmap.N))
    return mpl.colors.LinearSegmentedColormap.from_list(f'trimmed_{colormap}', colors)
