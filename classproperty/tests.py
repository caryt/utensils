"""Class Property  tests.

"""
from unittest import TestCase
from classproperty import classproperty


class MyClass(object):
    """A Test Class that cdefines a classproperty"""

    @classproperty
    @classmethod
    def foo(self):
        """Return Foo."""
        return "Foo"


class Test_classproperty(TestCase):
    """Test a :class:`.classproperty`."""

    def test_classproperty(self):
        """Test that a classproperty returns its value when accessed."""
        self.assertEqual(MyClass.foo, "Foo")