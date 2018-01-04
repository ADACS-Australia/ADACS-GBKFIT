import django
from django.core import signals
from django.core.handlers import base
from django.core.handlers.wsgi import WSGIRequest, get_script_name
from django.urls import set_script_prefix, resolve
from django.utils.encoding import force_str
import django.conf


class WSGIHandler(base.BaseHandler):
    request_class = WSGIRequest

    def __init__(self, *args, **kwargs):
        super(WSGIHandler, self).__init__(*args, **kwargs)
        self.load_middleware()

    def __call__(self, environ, start_response):

        # Generate a compatible url from the ROOT_SUBDIRECTORY_PATH
        pre_path = django.conf.settings.ROOT_SUBDIRECTORY_PATH
        if len(pre_path):
            # Confirm that the first character is a forward slash
            if pre_path[0] != '/':
                # No, insert a forward slash
                pre_path = "/" + pre_path

            # Confirm that the last character is not a forward slash
            if pre_path[-1] == '/':
                # Remove the forward slash
                pre_path = pre_path[:-1]

        # Override the environment paths
        environ['REQUEST_URI'] = "{}{}".format(pre_path, environ['REQUEST_URI'])
        environ['PATH_INFO'] = "{}{}".format(pre_path, environ['PATH_INFO'])

        set_script_prefix(get_script_name(environ))
        signals.request_started.send(sender=self.__class__, environ=environ)
        request = self.request_class(environ)

        response = self.get_response(request)

        response._handler_class = self.__class__

        status = '%d %s' % (response.status_code, response.reason_phrase)
        response_headers = [(str(k), str(v)) for k, v in response.items()]
        for c in response.cookies.values():
            response_headers.append((str('Set-Cookie'), str(c.output(header=''))))
        start_response(force_str(status), response_headers)
        if getattr(response, 'file_to_stream', None) is not None and environ.get('wsgi.file_wrapper'):
            response = environ['wsgi.file_wrapper'](response.file_to_stream)
        return response


def get_wsgi_application():
    """
    The public interface to Django's WSGI support. Should return a WSGI
    callable.

    Allows us to avoid making django.core.handlers.WSGIHandler public API, in
    case the internal WSGI implementation changes or moves in the future.
    """
    django.setup(set_prefix=False)
    return WSGIHandler()
