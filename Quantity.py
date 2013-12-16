"""Quantity
===========

.. inheritance-diagram:: Utilities.Quantity
"""
from Utilities.Null 					import Null
from fractions							import Fraction

class Unit(object):
	"""Unit is a base class that represents a unit for a Quantity.

	`unit`
		The name of this Unit (a string).
	`symbol`
		A symbol that can be used in place of the unit (e.g. the symbol for 'dollars' is '$')
	`converter`
		A converter class that knows how to convert between different units.

	"""

	def __init__(self, unit, symbol=Null, converter=Null):
		self.unit, self.symbol, self.converter = (str(unit), symbol, converter)
	def __str__(self):					return self.unit
	def __repr__(self):					return 'Unit({})'.format(self.unit)
	def __eq__(self, other):			return self.unit == getattr(other, 'unit', None)
	def __ne__(self, other):			return self.unit != getattr(other, 'unit', None)
	def units(self, number):
		"""Return the unit name formatted as a String. (**Note:** This handles plural forms)."""
		return _.plural(float(number), str(self.unit)) if self.symbol is Null else self.symbol

class FormatSpecs(object):
	"""Mixin class to extend the Format Specification mini-language."""

	def splitOff(self, spec, id):
		"""Split the new format specifier `id` out from the format `spec`."""
		return spec[:-1] if spec is not None and spec.endswith(id) else spec

	def format_i(self, value, spec):
		"""Format `:i` format displays it in integer format, if possible. e.g. `5.00%:i` -> 5%."""
		return ''.join((str(int(value)), self.formatUnits)) if self.splitOff(spec, 'i') != spec and (float(value) % 1 == 0.0) else None

	def format_b(self, value, spec):
		"""Format `:b` format displays it as blank when zero. e.g. `0.00:b` -> ."""
		return ' ' if self.splitOff(spec, 'b') != spec and (float(value) == 0.0) else None

	def format_k(self, value, spec):
		"""Format a PayRate Rate, shortening $1,000's to $k's, e.g. $50,000pa -> $50k."""
		return value._format_k.format(float(value)/1000.0) if self.splitOff(spec, 'k') != spec and float(value) % 1000.0 == 0.0 else None

	def format_rate(self, value, spec):
		"""Support a */rate* format specification, i.e. `{value:spec/rate}`."""
		spec, rate_format			= spec.split('/') if '/' in spec else (spec, '')
		return format(value.conversion(rate_format), spec) if rate_format else None

	def parse_spec(self, spec):
		"""Drop the new format specs. They are only only processed when called explicitly from a Qty sub-class."""
		spec						= self.splitOff(spec, 'i')
		spec 						= self.splitOff(spec, 'k')
		spec 						= self.splitOff(spec, 'b')
		return spec

	@property
	def div_format(self):
		"""Return a nice representation when dividing by a Quantity (overridden in Fractional_Quantity).

		See :class:`.Fractional_Quantity` for a nice fractional representation."""
		return '/{}'.format(self)


class Qty(FormatSpecs, object):
	"""Qty is a base class for objects with a value represented by some Units."""

	units 							= Unit('')
	"""The name of the units."""

	def __repr__(self):
		return '{}({}{})'.format(self.__class__.__name__, float(self), self.units.units(self))

	def __str__(self):
		"""Display Quantity as {value}{units}."""
		return ''.join((self.formatValue, self.formatUnits))

	#Conversion Routines
	def conversion(self, other):
		"""Describe a conversion, e.g. `{num:>10/hr}.format(10*dollars)` -> $10.00/hr."""
		return ''

	@property
	def formatValue(self):
		"""Return the formatted Quantity (value part only)."""
		return self._format()

	@property
	def formatUnits(self):
		"""Return the formatted Units part only."""
		return self.units.units(self)

	def __mul__(self, other):
		"""Handle `value * Quantity` and return the value represented by the appropriate units"""
		return other.__rmul__(self)

	def __eq__(self, other):
		"""Handle Qty == Qty, TODO doing units conversion as required."""
		return super(Qty, self).__eq__(other) if self.units == getattr(other, 'units', None) else False  # TODO - Unit conversions.

	def __ne__(self, other):
		return not (self == other)

	def __format__(self, spec):
		return format(str(self), self.parse_spec(spec))


class Float_Quantity(Qty, float):
	"""A real number in particular units. Quantity sub-classes override `units` and `__str__`."""
	def __new__(cls, value):		return float.__new__(cls, value)
	def __rmul__(self, other):		return self.__class__(float(other) * float(self))
	def _format(self, spec=None):	return format(float(self), spec if spec is not None else _.float_spec)
	def __format__(self, spec):
		"""Format this Float_Quantity. `:i` format displays it in integer format, if possible. e.g. `5.00:i` -> 5."""
		return self.format_i(self, spec) or Qty.__format__(self, spec)

	def __eq__(self, other):
		"""Handle Qty == Qty, (to 4dp). TODO doing units conversion as required."""
		return (abs(abs(float(self)) - abs(float(other))) < 0.0001) if self.units == getattr(other, 'units', None) else False  # TODO - Unit conversions.

	def __ne__(self, other):
		return not (self == other)

	words = {
				10**9: 	'billion',
				10**6: 	'million',
				10**3: 	'thousand',
				100:	'hundred',
				90:		'ninety',
				80:		'eighty',
				70:		'seventy',
				60:		'sixty',
				50:		'fifty',
				40:		'fourty',
				30:		'thirty',
				20:		'twenty',
				19:		'nineteen',
				18:		'eighteen',
				17:		'seventeen',
				16:		'sixteen',
				15:		'fifteen',
				14:		'fourteen',
				13:		'thirteen',
				12:		'twelve',
				11:		'eleven',
				10:		'ten',
				9:		'nine',
				8:		'eight',
				7:		'seven',
				6:		'six',
				5:		'five',
				4:		'four',
				3:		'three',
				2:		'two',
				1:		'one',
				0:		'',
				None:	'',
			}

	def _toWords(self):					return self.space(self.xillions(self, x) for x in (9, 6, 3, 0)) if self else ""
	def _toUnit(self, value, x):		return self.words[10**x if x else 0] if value != 0 else ""
	def _toWord(self, value, x):		return self.space((self.words[value], self._toUnit(value, x)))
	def conj(self, a, b):				return (" and " if a and b else "").join((a, b))
	def space(self, list):				return " ".join(word for word in list if word)
	def xillions(self, value, x):
		value 							= value // 10 ** x
		hundreds 						= (value % 1000) // 100
		tens 							= (value % 100) // 10 * 10
		ones 							= ((value % 100) % 10)
		teens 							= tens + ones if tens == 10 else None
		return self.space(( self._toWord(hundreds, 2),
							self._toWord(teens or tens, 0),
							self._toWord(ones, 0) if not teens else "",
							self._toWord(None, x) if value else "",
							str(self.units.unit) if x==0 else "",
							))

	@property
	def toWords(self):
		"""Return the number spelt out as words (e.g. *eleven* or *one hundred twenty three*)."""
		return self._toWords(self)

class Fixed_Quantity(Float_Quantity):
	"""A floating quantity in a non-specific *fixed* unit."""
	units = Unit('qty', symbol='')
qty = Fixed_Quantity(1.0)
"""Usage: e.g. `pieces = 40*qty`"""


class Percent_Quantity(Float_Quantity):
	"""A percentage. Transparently handles a divisor of 100. (e.g. `Percent(5)` is displayed as 5% and stored as 0.05)"""
	units 	= Unit('pct', symbol='%')
	def _format(self, spec=None):	return Float_Quantity._format(10000.0 * self)
	def __new__(cls, value):		return float.__new__(cls, value / 100.0)
	def __format__(self, spec):
		"""Format this Percent_Quantity. `:i` format displays it in integer format, if possible. e.g. `5.00%:i` -> 5%."""
		return self.format_i(self * 100.0, spec) or Float_Quantity.__format__(self, spec)
percent = Percent_Quantity(100.0)
"""Usage: e.g. `rate = 5 * percent`"""


class Fractional_Quantity(Qty, Fraction):
	"""A Fractional Quantity displays as a Fraction (e.g. 52/12).

	This is useful, for example, when converting months to weeks.
	"""

	def __new__(cls, num, den=1, preferred_denominator=None):
		return Fraction.__new__(cls, int(num), den)  # num may be a Qty

	def __init__(self, num, den=1, preferred_denominator=None):
		if hasattr(num, 'units'):
			self.units 					= num.units
		if preferred_denominator is not None:
			self.preferred_denominator 	= preferred_denominator

	def __repr__(self):
		return 'Qty({}/{}{})'.format(float(self._num), float(self._den), self.units.unit)

	def __invert__(self):
		"""Return the reciprical of the Fraction, keeping the same display preferences (e.g. ~52/12 = 12/52)."""
		inv 							= Fractional_Quantity(self.denominator, self.numerator)
		if hasattr(self, 'preferred_denominator'):
			inv.preferred_denominator 	= self._num
		if hasattr(self, 'units'):
			inv.units 					= self.units
		return inv

	def __mul__(self, other):
		"""Handle Fractional_Quantity * units."""
		if self.units.unit=='':
			#Handle normally when this Fraction has no units (e.g. 1/3 * $100.00)
			return other.__rmul__(self)
		if isinstance(other, float):
			#Handle 1. "Fraction * float"
			result 						= Fractional_Quantity(int(self.numerator*other), self.denominator)
			return result
		#Handle using normal logic.
		return other.__rmul__(self)

	def _format(self, spec=None):
		"""Format a Fractional_Quantity. 1/1 -> 1.00 and x/1 -> x."""
		if   float(self) == 1.0:		return '1.00'
		elif self._den   == 1.0: 		return '{0._num}'.format(self)
		return '{0._num:i}/{0._den:i}'.format(self)

	def preferred_repr(self):
		"""Fractions can be displayed with a preferred_demonimator, for convenience.
		This is instead of the standard python `limit_denominator` which uses the lowest possible denominator.
		e.g. 52 weeks / 12 months can be displayed as 52/12 rather than 13/3.
		"""
		result = Fraction(self).limit_denominator(self._pref)
		if self._pref % result.denominator == 0:
			return result.numerator * (self._pref / result.denominator), self._pref
		return result.numerator, result.denominator

	@property
	def div_format(self):
		"""Return a nice representation when dividing by a Fraction, e.g. /(52/12) -> \*12/52."""
		return '*{}'.format(~self)

	@property
	def _num(self):						return Float_Quantity(self.preferred_repr()[0])

	@property
	def _den(self):						return Float_Quantity(self.preferred_repr()[1])

	@property
	def _pref(self):					return getattr(self, 'preferred_denominator', self.denominator)
