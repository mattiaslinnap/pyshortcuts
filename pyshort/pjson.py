from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import json
import numpy as np


class NumpyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool):
            return bool(obj)
        for dtype in [np.int, np.int32, np.int64]:  # Could add more
            if isinstance(obj, dtype):
                return int(obj)
        for dtype in [np.float, np.float32, np.float64]:
            if isinstance(obj, dtype):
                return float(obj)
        if isinstance(obj, np.ndarray) and obj.ndim == 1:
            return list(obj)
        return super(NumpyJSONEncoder, self).default(obj)


def dumps(obj, *args, **kwargs):
    kwargs['cls'] = NumpyJSONEncoder
    return json.dumps(obj, *args, **kwargs)
