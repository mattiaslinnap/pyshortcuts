from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

from django.conf import settings
from django.core.mail import mail_managers

class RequestIpFromHttpXRealIp(object):
    """Middleware that sets request META['REMOTE_ADDR'] based on META['HTTP_X_REAL_IP'] if it exists.

    This header is set to client IP in typical Nginx proxy_params configuration.
    """
    def process_request(self, request):
        try:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
        except KeyError:
            pass

class MoreErrorEmails(object):
    """Middleware that emails managers for various response codes.

    Set SEND_EMAIL_ON_RESPONSE_CODES = [404, 403, ... ] in settings.py.
    """
    def process_response(self, request, response):
        """
        Send broken link emails for relevant 404 NOT FOUND responses.
        """
        if response.status_code in settings.SEND_EMAIL_ON_RESPONSE_CODES:
            domain = request.get_host()
            path = request.get_full_path()
            referer = request.META.get('HTTP_REFERER', '')
            ua = request.META.get('HTTP_USER_AGENT', '<none>')
            ip = request.META.get('REMOTE_ADDR', '<none>')
            mail_managers(
                "Error %s on %s" % (response.status_code, domain),
                "Referrer: %s\nRequested URL: %s\nUser agent: %s\nIP address: %s\n" % (referer, path, ua, ip),
                fail_silently=True)
        return response
