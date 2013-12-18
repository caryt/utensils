"""Test Null
============
"""
from unittest import TestCase
from null import Null

class TestNull(TestCase):
    """Test the :class:`.Null` object.
    """

    def assertNull(self, obj):
        return self.assertIs(obj, Null)

    def test_Null(self):
        """Test Null object."""
        self.assertNull(Null)
        self.assertNull(Null())
        self.assertNull(Null.foo)
        self.assertNull(Null(foo='foo', bar='bar'))
        self.assertNull(Null.foo(bar='bar'))
        self.assertNull(Null + 1)
        self.assertNull(Null - 1)
        self.assertNull(Null * 2)
        self.assertNull(Null / 2)
        self.assertNull(Null / 2)
        self.assertNull(Null // 2)
        self.assertNull(Null & 2)
        self.assertNull(Null | 2)
        self.assertNull(Null ^ 2)
        self.assertNull(Null >> 2)
        self.assertNull(Null << 2)
        self.assertNull(Null['foo'])
        self.assertNull(Null ** 2)
        self.assertNull(-Null)
        self.assertNull(+Null)
        self.assertNull(abs(Null))
        self.assertNull(~Null)

    def test_Equal(self):
        """Test Null object."""
        self.assertEqual(repr(Null),         'Null')
        self.assertEqual(str(Null),          'Null')
        self.assertEqual(Null.format('spec'), Null)
        self.assertEqual(Null.__html__(),    'Null')
        self.assertEqual(unicode(Null),     u'Null')
        self.assertEqual([x for x in Null], [])
        self.assertEqual(len(Null),   0)
        self.assertEqual(float(Null), 0.0)
        self.assertEqual(Null, Null)

    def test_False(self):
        """Test Null object."""
        self.assertFalse(Null < 0)
        self.assertFalse(Null == 0)
        self.assertFalse(Null == False)
        self.assertFalse(Null == None)
        self.assertFalse(Null == None)
        self.assertFalse(Null == [])
        self.assertFalse(Null == {})

    def test_True(self):
        """Test Null object."""
        self.assertTrue(Null == Null)
        self.assertTrue(Null is Null)

