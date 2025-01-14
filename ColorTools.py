"""
ColorTools.py

Personal utility functions to streamline customizing colors and cmaps in Matplotlib.
"""

import matplotlib
import numpy as np
from typing import List, Tuple, Union


def interpolate_colors(color_start: Union[str, Tuple[int, int, int]],
                       color_end: Union[str, Tuple[int, int, int]],
                       n: int) -> List[str]:
    """
    Interpolates between two given colors in N steps.
    Note: Cannot handle RGBA.

    Params:
        color_start: Hex string or RGB tuple for starting color
          color_end: Hex string or RGB tuple for ending color
                  n: Number of colors
    Returns:
        list of 'n' hex str colors interpolated from color_start to color_end.
    """

    def conv_to_rgb(c: Union[str, Tuple[int, int, int]]) -> Tuple[int, int, int]:
        """ Sets all passed RGB or Hex colors to an RGB tuple """
        if isinstance(c, str):  # Get & return RGB if hex
            return hex_to_rgb(matplotlib.colors.cnames.get(c, c))
        return c  # Return if already RGB

    cstart_rgb = conv_to_rgb(color_start)
    cend_rgb = conv_to_rgb(color_end)

    # Iterate over n ranage and lerp between colors.
    colors = []
    for i in range(n):
        fraction = i / float(n - 1)
        colors.append(rgb_to_hex([
            int(cstart_rgb[j] + (cend_rgb[j] - cstart_rgb[j]) * fraction)
            for j in range(3)
        ]))
    return colors


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """ Convert an RGB tuple to a hex color string """
    # Convert RGB colors to hexadecimal format
    return '0x{:02x}{:02x}{:02x}'.format(*rgb)


def hex_to_rgb(hex_in: str) -> Tuple[int, int, int]:
    """ Convert a hex color string to an RGB tuple """
    hex_in = hex_in.strip("#")
    return tuple(int(hex_in[i:i + 2], 16) for i in (0, 2, 4))


def trim_cmap(colormap: str, cmin: float=0.20, cmax: float=1.00) -> matplotlib.colors.LinearSegmentedColormap:
    """
    Trims an existing Matplotlib colormap to a subset of its range.

    Params:
        colormap: String of named Matplotlib colormap
            cmin: The Minimum value of the cmap range (between 0.0 and 1.0)
            cmax: The Maximum value of the cmap range (between 0.0 and 1.0)
    returns:
        A new LinearSegmentedColormap.
    """
    
    # Takes a Matplotlib Colormap and a min and max value
    # Returns trimmed version of that colormap to only the specified color space between 0.0 and 1.0
    cmap = matplotlib.colormaps[colormap]
    trimmed_colors = cmap(np.linspace(cmin, cmax, cmap.N))
    return matplotlib.colors.LinearSegmentedColormap.from_list(f'trimmed_{colormap}', trimmed_colors)
