# -*- coding : utf-8 -*-

from django.conf import settings
from raven.processors import Processor
from raven.utils import varmap
import urlparse

class SanitizeSensibleDatasProcessor(Processor):
    """
    Asterisk out sensibles datas from who could appear in HTTP requests
    or in stacktrace.
    """
    MASK = '*' * 16

    def sanitize(self, key, value):
        if not key:  # key can be a NoneType
            return value

        if key in settings.SENSIBLE_DATAS :
            # store mask as a fixed length for security
            return self.MASK

        return value

    def filter_stacktrace(self, data):
        if 'frames' not in data:
            return
        for frame in data['frames']:
            if 'vars' not in frame:
                continue
            frame['vars'] = varmap(self.sanitize, frame['vars'])

    def filter_http(self, data):
        for n in ('body', 'cookies', 'headers', 'env'):
            if n not in data:
                continue

            data[n] = varmap(self.sanitize, data[n])
    
    def filter_request(self, data) :
        """To filter all the http requests and urls to hide parameters."""
        
        if 'extra' in data :
        # Clean the request in datas?
            if 'request' in data['extra'] :
                del data['extra']['request']
        
        if 'sentry.interfaces.Http' in data :
            if 'url' in data['sentry.interfaces.Http'] :
                # To keep URL who causes problem but without the parameters.
                parsed_url = urlparse.urlparse(data['sentry.interfaces.Http']['url'])
                data['sentry.interfaces.Http']['url'] = urlparse.urlunparse((parsed_url[0], parsed_url[1], parsed_url[2], '', '', ''))
            if 'query_string' in data['sentry.interfaces.Http'] :
                # clean the string who contains query.
                del data['sentry.interfaces.Http']['query_string']
        
        if 'sentry.interfaces.Stacktrace' in data :
        # Clean the stack of requests
            if 'frames' in data['sentry.interfaces.Stacktrace'] :
                for vars in data['sentry.interfaces.Stacktrace']['frames'] :
                    if 'vars' not in vars :
                        continue
                    if 'request' in vars['vars'] :
                        del vars['vars']['request']
                        
    def process(self, data, **kwargs):
        if 'sentry.interfaces.Stacktrace' in data:
            self.filter_stacktrace(data['sentry.interfaces.Stacktrace'])

        if 'sentry.interfaces.Http' in data:
            self.filter_http(data['sentry.interfaces.Http'])
        
        self.filter_request(data)

        return data