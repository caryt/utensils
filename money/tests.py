"""Test Money
=============
"""
from unittest import TestCase
from money import Dollars, Cents

dollars = Dollars(1.0)
cents=Cents(1)

class TestDollars(TestCase):
    """Test a :class:`.Dollars`.
    """

    def test_test(self):
        """Test."""
        self.assertEqual(5*dollars, Dollars(5.0))
        self.assertEqual(str(5*dollars), "$5.00")
        self.assertEqual(float(5*dollars), 5.00)
        self.assertEqual(5*dollars + 3*dollars, 8*dollars)
        self.assertEqual(5*dollars - 3*dollars, 2*dollars)
        self.assertEqual(abs(-5*dollars), 5*dollars)
        self.assertEqual(5*dollars * 3, 15*dollars)
        self.assertEqual(Dollars.fromString("1,234.56"), 1234.56*dollars)
        self.assertEqual(Dollars.fromString("1,234.56").dollars, 1234*dollars)
        self.assertEqual(Dollars.fromString("1,234.56").round_dollars, 1235*dollars)
        self.assertEqual(Dollars.fromString("1,234.56").round_dollars, 1235*dollars)
        # self.assertEqual(Dollars.fromString("1,234.56").cents, 56*cents)
        self.assertEqual(Dollars.fromString("1,234.56").asCents, 123456)
        self.assertEqual(Dollars.fromString("1,234.56").toWords,
            "one thousand two hundred thirty four dollars and fifty six cents")
