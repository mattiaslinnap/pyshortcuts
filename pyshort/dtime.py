"""NOTE: see djangoshortcuts/dtime.py for timezone-aware conversions."""
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import datetime


def dtime(millis_since_1970):
    """Returns a timezone-unaware datetime in UTC for a unix timestamp (milliseconds since 1970)."""
    millis = float(millis_since_1970)  # In case it's a numpy datatype
    return datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=millis)


def unixtime(dt):
    """Returns milliseconds since 1970 for datetime dt."""
    return int(1000 * (dt - datetime.datetime(1970, 1, 1)).total_seconds())
