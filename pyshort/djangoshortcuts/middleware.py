from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

class RequestIpFromHttpXRealIp(object):
    """Middleware that sets request META['REMOTE_ADDR'] based on META['HTTP_X_REAL_IP'] if it exists.

    This header is set to client IP in typical Nginx proxy_params configuration.
    """
    def process_request(self, request):
        try:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
        except KeyError:
            pass

