"""WSGI Application
===================
"""
from uri import URI
from werkzeug.wrappers import Response
from werkzeug.exceptions import HTTPException
from werkzeug.serving import run_simple
from cherrypy import wsgiserver
from routes import url_map
from traceback import format_exc
from werkzeug.test import create_environ

HTML = 'text/html'
"Content-Type for HTML documents."""

TEXT = 'text/plain'
"Content-Type for plaintext documents."""


class WSGIApplication(object):
    """This is the root `Werkzeug`_ WSGI application object that
    accepts web requests, dispataches them using it's `url_map` or
    routing rules.

    .. _Werkzeug: http://werkzeug.pocoo.org/

    .. inheritance-diagram:: WSGIApplication
    """

    url_map = url_map()

    HTML = HTML
    TEXT = TEXT

    def __init__(self):
        self.mimetype = None
        self.response = None

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        """The main entry point for handling a web request.
        Sets up the `environ`, dispatches the request depending
        on the Routing Rules stored in `url_map` and converts
        exceptions to HTTP Errors.
        """
        urls = self.url_map.bind_to_environ(environ)
        try:
            self.response = None
            endpoint, args = urls.match()
            data = self.dispatch(environ, start_response, endpoint, args)
            if not self.response:
                self.response = Response(data, mimetype=self.mimetype)
            return self.response(environ, start_response)
        except HTTPException, exception:
            return exception(environ, start_response)
        except Exception, e:
            return self.handle_exception(environ, start_response, e)

    def handle_exception(self, environ, start_response, e):
        """Handle an exception at this top level.
        In debug mode print a shortened traceback
        suitable for a debug message on the client.
        """
        if self.debugging:
            #Print the traceback to stdout for debugging...
            print format_exc()
            #Return a shortened traceback, for debugging on the client...
            self.response = Response(format_exc(2), mimetype=TEXT, status=500)
            return self.response(environ, start_response)
        raise e

    def start_server(self, arg=None):
        """Start the (production grade) CherryPy web server."""
        server = wsgiserver.CherryPyWSGIServer(self.config.host, self)
        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()

    def run_simple(self, arg=None):
        """Start a simple (testing / development) server."""
        host, port = self.config.host
        run_simple(host, port, self, use_debugger=True, use_reloader=True)

    def base(self, environ):
        """Return the base URL for the application."""
        return URI.fromParts(
            environ['wsgi.url_scheme'],
            self.config.PUBLIC_HOST,
            self.config.PUBLIC_PORT,
            default=80,
        )

    @property
    def test_environ(self):
        """Return a Test WGSI environment."""
        return create_environ('/test', None)

