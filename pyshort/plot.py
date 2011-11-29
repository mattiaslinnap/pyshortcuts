#!/usr/bin/python
'''
Utilities for matplotlib.
'''
from __future__ import division

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
