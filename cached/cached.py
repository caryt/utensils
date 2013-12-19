"""Cached
=========
"""
class cached(object):
    """A decorater that replaces a method with it's value,
    so only the first access does the (expensive) calculation.
    Usage::

        @cached
        def expensive(self):
            return some_expensive_calculation

    To invalidate the cache, use::

        del obj.expensive

    """
    def __init__(self, fget):
        self.fget       = fget
        self.__doc__    = fget.__doc__

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self.fget(obj)
        setattr(obj, self.fget.func_name, value)
        return value