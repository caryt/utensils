"""Lookup
=========

.. inheritance-diagram:: Utilities.Lookup
"""
from bisect 								import bisect_left, bisect_right
from Utilities.Null							import Null


class Over(object):
	"""A High Value, useful for the final entry in Lookup tables."""
	def __repr__(self): 					return 'Over'
	def __gt__(self, other):				return True
	def __eq__(self, other):				return other is Over
	def __lt__(self, other):				return False
Over = Over()


class Lookup(object):
	"""A Lookup table is an ordered list of (key, value) pairs. Looking up an item matches the first key **less than or equal to** the item.

	E.g. If aTable = ((100, 5), (200, 10), (500, 50)) then aTable[1] == 5, aTable[150] == 10, aTable[499] == 50.
	"""
	def __init__(self, *table):
		if table is not None: 				self.table = table

	def __getitem__(self, item):
		try:
			return self.table[self._lookup(item)][1]
		except IndexError:
			return Null
	def _lookup(self, item):				return bisect_right(self.table, (item,))
	def __repr__(self):						return '\n'.join('<= {}\t {}'.format(k, v) for (k, v) in self.table)


class LookupLessThan(Lookup):
	"""A Lookup table is an ordered list of (key, value) pairs. Looking up an item matches the first key **less than** the item.

	E.g. If aTable = ((100, 5), (200, 10), (500, 50)) then aTable[1] == 5, aTable[150] == 10, aTable[499] == 50.
	"""
	def _lookup(self, item):				return bisect_left( self.table, (item, Over))
