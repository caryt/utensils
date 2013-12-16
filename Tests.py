"""Testing Utilities
====================
"""
import unittest


class MultipleTests(unittest.TestCase):
	"""A Test Case that can automatically generate a number of Tests."""

	@classmethod
	def fn_name(cls, check_fn, args, result):
		"""Return a name for the check_fn for an individual test. (NB: must start with "test")."""
		name = "test_%s_%r_%r" % (check_fn.__name__, args, result)
		return name.translate(None, "<>()',").replace(' ', '_').replace(".", "_")

	@classmethod
	def generate_test(cls, check_fn, args, result):
		"""Generate an individual test, and add it to this TestCase."""
		setattr(cls, cls.fn_name(check_fn, args, result), lambda self: check_fn(self, args, result))
