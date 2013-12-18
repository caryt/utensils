"""REST Interface
=================
Implements :class:`RESTful` - a Base Class for objects implementing a
`RESTful`_ inteface.

.. _RESTful: http://en.wikipedia.org/wiki/REST
.. _CRUD: http://en.wikipedia.org/wiki/Create,_read,_update_and_delete
"""
from crud import CRUD
from registered import Registered
from werkzeug.exceptions import MethodNotAllowed


class REST(object):
    """Mix-in class to implement REST HTTP Verbs."""
    HTTP_METHODS = {'GET', 'PUT', 'POST', 'DELETE'}
    """Valid HTTP Methods."""

    def GET(self, **args):
        """Read and return details for an object via the Web.
        """
        raise MethodNotAllowed

    def POST(self, **args):
        """Create a new object via the Web."""
        raise MethodNotAllowed

    def PUT(self, **args):
        """Update an existing object via the Web."""
        raise MethodNotAllowed

    def DELETE(self, **args):
        """Delete an object via the Web."""
        raise MethodNotAllowed

    def LIST(self):
        """Read and return details for **all** objects.
        """
        raise MethodNotAllowed

    def isCollection(self):
        """Return True if this HTTP request is for a collection."""
        return False

    def method(self, method, **args):
        """Return HTTP method for this request."""
        list = (method=='GET' and self.isCollection(**args))
        return 'LIST' if list else method

    def __call__(self, method, **args):
        if method in self.HTTP_METHODS:
            return getattr(self, self.method(method, **args))(**args)


class RESTful(REST, CRUD):
    """A RESTful object is a base class for objects that implement a
    REST interface. This interface exposes the classic `CRUD`_
    (Create, Read, Update, Delete and, additionally, List) operations
    via the web using HTTP Method
    (GET=read, PUT=update, POST=create, DELETE=delete).

    .. inheritance-diagram:: RESTful
    """
    __metaclass__ = Registered

    @property
    def db(self):
        """Return the Application's database object."""
        return self.app.db

    @property
    def json(self):
        """Return the JSON document passed in via the HTTP Request."""
        return self.environ['werkzeug.request'].json
