'''
Utilities for matplotlib.
'''
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

from matplotlib import pyplot as pp
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
