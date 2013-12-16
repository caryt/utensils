"""Registered
=============
"""
from Utilities.Null import Null


class Registered(type):
    """A meta-class for classes that keep a Registry of their sub-classes.
    This allows the creation of subclasses by name. E.g.:

        |   class BaseClass(object):
        |      __metaclass__ = Registered
        |
        |   class SubClass1(BaseClass): pass
        |   class SubClass2(BaseClass): pass
        |
        |   BaseClass['SubClass1']

    A Registered class can also be iterated over for all its
    Registered subclasses, Usage:

            | for subclass in cls
    """
    _Registry = {}
    """A mapping of a string to a Class."""

    def __init__(cls, name, bases, dct):
        """Register the `cls` in the Registry."""
        #Create a registry for *this* class
        cls._Registry = {}
        #Insert a reference to this class in it's *base class'* registry
        cls._super(bases)._Registry[name] = cls

    def _super(cls, bases):
        """Return the base class that implements the Registry."""
        super = [base for base in bases if isinstance(base, Registered)]
        return super[0] if len(super) else Registered

    def __getitem__(cls, name):
        """Return a :class:`.Registered` class of the classname `name`.
        ("name" or "Name" can be passed to return a class called "Name").
        """
        return cls._Registry.get(cls.classCase(name), Null)

    def __iter__(cls):
        """Return an iterator over all Registered subclasses, Usage:
            | for subclass in cls
        """
        return iter(cls._Registry.values())

    def classCase(cls, name):
        return name[0].upper() + name[1:]

    def __contains__(cls, key):
        """Return True if `key` is the name of a Registered subclass."""
        return cls.classCase(key) in cls._Registry

