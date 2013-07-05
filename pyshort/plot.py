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

# Figure sizes for A4 paper.
A4 = cm(21.0), cm(29.7)
A4_LANDSCAPE = cm(29.7), cm(21.0)


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


def density_plot(ax, x, y_samples, percentile_step=5, cmap=mcm.Blues):
    """Plots density, as sort of a heatmap with linear filled lines.

    y_samples must be a 2-dimensional array. Each row is one x value, and each column is a sample from some y distribution.
    percentile_step ought to divide into 100 evenly.
    """
    num_x = len(y_samples)
    percentiles = range(0, 100 + percentile_step, percentile_step)
    assert len(percentiles) % 2 == 1
    assert 0 in percentiles
    assert 50 in percentiles
    assert 100 in percentiles

    # List of arrays. Each list is for a percentile, each array element is y value at x.
    y_list = np.percentile(y_samples, percentiles, axis=1)
    assert len(y_list) == len(percentiles)
    for i in xrange(len(percentiles) - 1):
        y1 = y_list[i]
        y2 = y_list[i + 1]
        # Color distance ranges from 0.0 to 1.0 to 0.0 as percentile goes 0-50-100.
        if i < len(percentiles) / 2:
            # Color based on next percentile (line below)
            color = cmap(percentiles[i + 1] / 50)
        else:
            # Color based on this percentile (line above)
            color = cmap((100 - percentiles[i]) / 50)
        ax.fill_between(x, y1, y2, color=color)







