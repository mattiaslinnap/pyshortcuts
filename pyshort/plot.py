'''
Utilities for matplotlib.
'''
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import logging
import matplotlib
from matplotlib import cm as mcm
import numpy as np
import sys


logger = logging.getLogger(__name__)


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


def cms(width, height):
    return cm(width), cm(height)


# Figure sizes for A4 paper.
A4 = cms(21.0, 29.7)
A4_LANDSCAPE = cms(29.7, 21.0)


def rc_print_settings():
    """Configures fonts, text sizes and line widths for figures inserted into A4 papers."""
    matplotlib.rc('text', usetex=True)
    matplotlib.rc('font', family='serif', serif=['Computer Modern Roman'], size=10)
    matplotlib.rc('lines', linewidth=0.5)  # Plots
    matplotlib.rc('patch', linewidth=0.5)  # Polygons, for example legend
    matplotlib.rc('axes', linewidth=0.5)  # Axis borders and ticks
    matplotlib.rc('legend', fontsize=6)
    matplotlib.rc('figure', autolayout=True)
    matplotlib.rc('savefig', dpi=300, format='pdf', bbox='tight')


def hist_fixed_bins(axes, data, bins, log=False, open_end=False, normed=False, color='b', alpha=1.0, label=None, ticklabels=None, ticklabels_interval=1):
    """Plots a histogram with given bins, but equal plotted bin widths.
    Useful if bin widths are very unequal.
    open_end=True appends a bin edge at +infinity.
    normed=True makes the values a probability *mass* function: bin counts are divided by the total number of data points (the sum of y values will sum to 1.0).
    If ticklabels is None, tick labels are shown for every ticklabels_interval bin. The first and inf are always shown.
    """
    if open_end:
        bins = bins + [float('inf')]

    hist, _ = np.histogram(data, bins=bins)
    if normed:
        hist = np.array(hist, dtype=np.float64)
        hist /= len(data)
    axes.bar(range(len(hist)), hist, width=0.99, log=log, color=color, alpha=alpha, label=label)
    axes.set_xticks(range(len(bins)))
    if ticklabels is None:
        ticklabels = [str(b) for b in bins]
        ticklabels[-1] = ''
        for i in xrange(1, len(ticklabels) - 1):  # Always keep first and last label.
            if i % ticklabels_interval != 0:
                ticklabels[i] = ''
        ticklabels[-2] = ticklabels[-2] + '+'
    axes.set_xticklabels(ticklabels)
    axes.set_xlim(0, len(bins) - 1)


def set_color_cycle_from_cmap(axes, cmap_name='spectral', num_colors=10, repeat_each=1):
    """Sets an alternative color cycle for multiple calls to pyplot.plot()."""
    cmap = mcm.get_cmap(cmap_name)
    colors = []
    for arg in np.linspace(0, 0.9, num_colors):
        for i in xrange(repeat_each):
            colors.append(cmap(arg))
    axes.set_color_cycle(colors)


def _percentile_values(y_samples, percentile_step):
    """Computes percentiles for samples.

    y_samples should be a 2D numpy array or a list of lists of samples.
    Each row (outer list) is for one X value, and each column (inner list) is a sample of Y values at that X.

    Returns the percentiles list, and a list of numpy arrays.
    The each outer list element is for one percentile value. Each array element is the Y at that percentile for each X.
    """
    percentiles = range(0, 100 + percentile_step, percentile_step)
    assert len(percentiles) % 2 == 1
    assert 0 in percentiles
    assert 50 in percentiles
    assert 100 in percentiles

    if isinstance(y_samples, np.ndarray):
        assert len(y_samples.shape) == 2, 'y_samples must be a 2D numpy array or a list of lists of numbers.'
        assert len(y_samples) > 0, 'y_samples must not be empty.'
        assert len(y_samples[0]) > 0, 'y_samples must not be empty.'
    else:
        assert isinstance(y_samples, list), 'y_samples must be a 2D numpy array or a list of lists of numbers.'
        assert y_samples, 'y_samples must not be empty.'
        for ys in y_samples:
            assert isinstance(ys, list), 'y_samples must be a 2D numpy array or a list of lists of numbers.'
            assert ys, 'y_samples must not have empty inner lists, each X value must have at least one Y sample.'
        if len(set(len(ys) for ys in y_samples)) == 1:
            # All y_samples rows have the same length. Can convert into a numpy array for fast percentile computation.
            y_samples = np.array(y_samples)

    # y_list is a list of arrays. Each list is for a percentile, each array element is y value at x.
    if isinstance(y_samples, np.ndarray):
        # y_samples is a numpy array, can compute percentiles in one go.
        y_list = np.percentile(y_samples, percentiles, axis=1)
    else:
        # y_samples is a list of lists of uneven lengths. Slow mode.
        logger.warning('Slow percentile computation: consider switching to 2D numpy arrays.')
        num_x = len(y_samples)
        y_list = []
        for p in percentiles:
            y_list.append(np.zeros(num_x, dtype=np.float64))
            for i in xrange(num_x):
                y_list[-1][i] = np.percentile(y_samples[i], p)

    assert len(y_list) == len(percentiles)
    return percentiles, y_list


def density_fill_plot(ax, xs, y_samples, percentile_step=5, cmap=mcm.Blues, label=None):
    """Plots density, as sort of a heatmap with linear filled lines.

    y_samples must be a 2-dimensional array. Each row is one x value, and each column is a sample from some y distribution.
    percentile_step ought to divide into 100 evenly.
    """
    assert len(xs) == len(y_samples)
    num_x = len(xs)
    assert num_x > 0

    percentiles, y_list = _percentile_values(y_samples, percentile_step)

    for i in xrange(len(percentiles) - 1):
        y1 = y_list[i]
        y2 = y_list[i + 1]
        pct = percentiles[i] + percentile_step / 2

        # Color distance ranges from 0.0 to 1.0 to 0.0 as percentile goes 0-50-100.
        if pct <= 50:
            distance = pct / 50
        else:
            distance = (100 - pct) / 50
        assert distance >= 0.0
        assert distance < 1.0
        color = cmap(distance)[:3]  # Remove alpha
        alpha = distance
        ax.fill_between(xs, y1, y2, color=color, alpha=alpha)
    ax.plot(xs, y_list[len(percentiles) // 2], color=cmap(1.0), label=label)


def density_line_plot(ax, xs, y_samples, percentile_step=5, color='b', label=None):
    """Plots density, as individual thin lines for percentiles.

    y_samples must be a 2-dimensional array. Each row is one x value, and each column is a sample from some y distribution.
    percentile_step ought to divide into 100 evenly.
    """
    assert len(xs) == len(y_samples)
    num_x = len(xs)
    assert num_x > 0

    percentiles, y_list = _percentile_values(y_samples, percentile_step)

    for i in xrange(len(percentiles)):
        y = y_list[i]
        # Alpha ranges from 0.0 to 1.0 to 0.0 as percentile goes 0-50-100.
        if i <= len(percentiles) / 2:
            # Alpha based on next percentile (line below)
            alpha = percentiles[i] / 50
        else:
            # Color based on this percentile (line above)
            alpha = (100 - percentiles[i]) / 50
        if percentiles[i] == 50:
            ax.plot(xs, y, color=color, alpha=alpha, label=label)
        else:
            ax.plot(xs, y, color=color, alpha=alpha)



