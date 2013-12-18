"""Plural
=========

.. inheritance-diagram:: Plural
"""
#TODO - See http://pypi.python.org/pypi/inflect for lots more possibilities....

class Plural(object):
	"""Base class to return the plural form of a number. Sub-classed for specific languages."""

	@classmethod
	def single(cls, singular, plural):
		"""Return the singular form for a number."""
		return singular

	@classmethod
	def dual(cls, singular, plural):
		"""Return the dual form for a number. (In this default class, it is just the singular form if a plural form isn't specified)."""
		return singular if (plural is None) else plural

	@classmethod
	def multiple(cls, singular, plural):
		"""Return the multiple form for a number. (In this default class, it is just the dual form)."""
		return cls.dual(singular, plural)

	@classmethod
	def plural(cls, number, singular, plural=None):
		"""Return the appropriate singular/plural form.

		Note the special case. If singular is blank, always return blank.
		"""
		if   singular == '': 		return ''
		elif abs(number)==1: 		return cls.single(singular, plural)
		elif abs(number)==2:		return cls.dual(singular, plural)
		return cls.multiple(singular, plural)

	@classmethod
	def indefinite(cls, noun):
		"""Return the indefinite article for this noun (i.e. a or an).

		Actually, returns '' or 'n", as this allows format strings to be written as "a{n}"."""
		return 'n' if str(noun)[0].lower() in 'aeiou' else ''


class EnglishPlural(Plural):
	"""Return the English plural form for a number.

	Usage:
		`EnglishPlural.plural(2, 'person', 'people')` -> *people*.
		`EnglishPlural.plural(2, 'apple')` -> *apples*.
		`EnglishPlural.plural(1, 'apple')` -> *apple*.
	"""

	@classmethod
	def dual(cls, singular, plural):
		"""Plural forms in English are the singular with an 's' appended, or the plural form."""
		return (singular + 's') if (plural is None) else plural

