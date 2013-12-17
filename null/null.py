"""Null Object
==============
"""


class _Null(object):
    """Null object is a singleton that does nothing, returning itself in response to all operations."""

    def __getattr__(self, attr):
        try:
            return super(self.__class__, self).__getattr__(attr)
        except AttributeError:
            if attr in ('__base__', '__bases__', '__basicsize__', '__cmp__',
                        '__dictoffset__', '__flags__', '__itemsize__',
                        '__members__', '__methods__', '__mro__', '__name__',
                        '__subclasses__', '__weakrefoffset__',
                        '_getAttributeNames', 'mro'):
                raise
            else:
                return self
    def next(self):							raise StopIteration
    def __repr__(self):                     return 'Null'
    def __str__(self):                      return 'Null'
    def __html__(self):                     return 'Null'  # For Jinja2 templates
    def __unicode__(self):                  return u'Null'
    #def __reduce__(self):                   return 'Null'
    def __init__(self, *args, **kwargs):	pass
    def __len__(self):						return 0
    def __eq__(self, other):				return self is other
    def __hash__(self):						return hash(None)
    def __call__(self, *args, **kwargs):	return self
    def __float__(self):                    return 0.0
    def __lt__(self, other):                return False
    def __format__(self, spec):
        try:
            return format(repr(self), spec)
        except:
            return repr(self)
    __sub__     = __div__   = __mul__   = __floordiv__  = __mod__       = __and__   = __or__ = \
    __xor__     = __rsub__  = __rdiv__  = __rmul__      = __rfloordiv__ = __rmod__  = \
    __rand__    = __rxor__  = __ror__   = __radd__      = __pow__       = __rpow__  = \
    __rshift__  = __lshift__= __rrshift__ = __rlshift__ = __truediv__   = \
    __rtruediv__= __add__   = __getitem__ = __neg__     = __pos__       = __abs__   = \
    __invert__  = __setattr__ = __delattr__ = __delitem__ = __setitem__ = \
    __iter__    = __call__

Null = _Null()
"""The Null object. A singleton that does nothing, returning itself in response to all operations. E.g.:

* :code:`Null.attr` returns Null for *any* attr
* :code:`Null + obj` or :code:`obj + Null` returns Null (similarly - * / etc.)
* :code:`Null.method(args)` returns Null for *any* method call
* :code:`obj == Null` returns False (unless obj is Null)
* :code:`obj < Null` returns False
* :code:`repr(Null)` returns "Null"
* :code:`Null.format(spec)` returns "Null" and will support string formatting specs (e.g. :width)

Null objects are useful when coding as they can eliminate many checks for `if obj is None`."""
