"""Validators
=============

:class:`.Validators` implements many input validation methods.

.. inheritance-diagram:: Utilities.Validators

"""
from Utilities.Date 					import *
from jinja2.utils 						import escape


class Validators(dict):
	"""Implementation for various Validation methods, mix-in for :class:`.Validate`."""

	def isa(self, cls, field, msg=None):
		"""Check that the field is a `cls`.
		This uses `cls.fromString` to validate the field, and convert it into an instance of `cls`
		"""
		msg 							= msg or '{field} must be a valid %s, not {value}.' % cls.__name__
		return self._try(lambda f: cls.fromString(f), field, msg)

	def equalValues(self, value1, value2, msg):
		"""Check that `value` is equal to `value2`."""
		if value1 != value2:
			return self.message(msg, None)
		return True

	def match(self, field, field2):
		"""Check that `field` is equal to `field2`."""
		self[field]						= self.form[field]
		self[field2]					= self.form[field2]
		if self[field] != self[field2]:
			return self.message('{field} and {field2} must match'.format(field='{field}', field2=field2), field)
		return True

	def required(self, field):
		"""Check that the field contains a value."""
		self[field]						= self.form[field]
		if not self.form[field].strip():
			return self.message('{field} must be present.', field)
		return True

	def string(self, field):
		"""Check that the field is a string (anything goes - but strings are escaped for XSS protection)."""
		return self._try(lambda f: str(escape(f)), field, '{field} must be a string.')

	def numeric(self, field):
		"""Check that the field is numeric."""
		return self._try(lambda f: float(f), field, '{field} must be a number, not {value}.')

	def date(self, field, optional=False):
		"""Check that the field is a date."""
		if optional and not self.form[field].strip():
			self[field] 				= None
		else:
			return self.isa(Date, field)
		return True

	def currency(self, field):
		"""Check that the field is Money."""
		return self.isa(_.Currency, field, msg='{field} must be a valid amount, not {value}.')

	def rate(self, field, Value, Units):
		"""Check that the field is a valid Rate."""
		if Value(field):				return self._rate(Units, field)
		return False

	def quantity(self, field, Value, Units):
		"""Check that the field is a valid Quantity."""
		if Value(field):				return self._units(Units, field)
		return False

	def costcentre(self, field):
		"""Check that the field is a valid Costcentre."""
		return self.string(field)  # TODO - Implement

	def email(self, field):
		"""Check that the field looks like an email address (Note: This *doesn't* validate the address)."""
		result = self.string(field)
		if '@' not in self[field]:
			return self.message('{field} must be a valid email address (with an "@"), not {value}', field)
		return result

#TODO - eq, ne, le, lt, gt, ge, past, future, in, not in, int, float
