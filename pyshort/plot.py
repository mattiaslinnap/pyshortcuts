'''
Utilities for matplotlib.
'''
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

from matplotlib import cm as mcm
from matplotlib import pyplot as pp
import numpy as np
import sys

def close_figure_on_key(figure):
    """Attaches keyboard events to quit to the figure. Clicking X is annoying.""" 
    def on_key(event):
        if event.key in ['escape', 'q']:
            sys.exit()
    figure.canvas.mpl_connect('key_release_event', on_key)

def vertical_x_labels(axes):
    """Makes x labels vertical. Useful if they are long strings."""
    for tl in axes.get_xticklabels(): 
        tl.set_rotation(-90)

def cm(centimetres):
    """Actually returns inches from cm. Named like this to give impression of units.

    Usage:
    pyplot.figure(figsize=(cm(10), cm(5))
    """
    return centimetres / 2.54

def a4():
    """Returns a figsize for A4 paper.

    Usage:
    pyplot.figure(figsize=a4())
    """
    return cm(21.0), cm(29.7)
A4 = a4()

def hist_fixed_bins(axes, data, bins, log=False, open_end=False):
    """Plots a histogram with given bins, but equal plotted bin widths.
    Useful if bin widths are very unequal.
    open_end=True appends a bin edge at +infinity.
    """
    if open_end:
        bins = bins + [float('inf')]

    hist, _ = np.histogram(data, bins=bins)
    axes.bar(range(len(hist)), hist, width=0.99, log=log)
    axes.set_xticks(range(len(bins)))
    axes.set_xticklabels([str(b) for b in bins])

def set_color_cycle_from_cmap(axes, cmap_name='spectral', num_colors=10, repeat_each=1):
    """Sets an alternative color cycle for multiple calls to pyplot.plot()."""
    cmap = mcm.get_cmap(cmap_name)
    colors = []
    for arg in np.linspace(0, 0.9, num_colors):
        for i in xrange(repeat_each):
            colors.append(cmap(arg))
    axes.set_color_cycle(colors)

