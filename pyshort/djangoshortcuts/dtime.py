from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import datetime
from django.utils.timezone import utc

def aware_datetime(millis_since_1970):
    """Returns a timezone-aware datetime in UTC for a unix timestamp (milliseconds since 1970)."""
    return (datetime.datetime(1970,1,1) + datetime.timedelta(milliseconds=millis_since_1970)).replace(tzinfo=utc)
