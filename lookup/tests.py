"""Lookup tests.

"""
from unittest import TestCase
from lookup import Lookup, LookupLessThan, Over

class Test_Lookup(TestCase):
    """Test a Lookup Table (that uses Less Than or Equal To)."""

    def setUp(self):
        self.lookup = Lookup((100, 5), (200, 10), (500, 50), (Over, 99))

    def test_Lookup_50( self): self.assertEqual(self.lookup[ 50],  5)
    def test_Lookup_99( self): self.assertEqual(self.lookup[ 99],  5)
    def test_Lookup_100(self): self.assertEqual(self.lookup[100],  5)
    def test_Lookup_101(self): self.assertEqual(self.lookup[101], 10)
    def test_Lookup_200(self): self.assertEqual(self.lookup[200], 10)
    def test_Lookup_201(self): self.assertEqual(self.lookup[201], 50)
    def test_Lookup_500(self): self.assertEqual(self.lookup[500], 50)
    def test_Lookup_501(self): self.assertEqual(self.lookup[501], 99)
    def test_Lookup_999(self): self.assertEqual(self.lookup[999], 99)

class Test_LookupLessThan(TestCase):
    """Test a Lookup Table (that uses strict Less Than)."""

    def setUp(self):
        self.lookup = LookupLessThan((100, 5), (200, 10), (500, 50), (Over, 99))

    def test_Lookup_50( self): self.assertEqual(self.lookup[ 50],  5)
    def test_Lookup_99( self): self.assertEqual(self.lookup[ 99],  5)
    def test_Lookup_100(self): self.assertEqual(self.lookup[100], 10)  # Not 5
    def test_Lookup_101(self): self.assertEqual(self.lookup[101], 10)
    def test_Lookup_200(self): self.assertEqual(self.lookup[200], 50)  # Not 10
    def test_Lookup_201(self): self.assertEqual(self.lookup[201], 50)
    def test_Lookup_500(self): self.assertEqual(self.lookup[500], 99)  # Not 50
    def test_Lookup_501(self): self.assertEqual(self.lookup[501], 99)
    def test_Lookup_999(self): self.assertEqual(self.lookup[999], 99)
