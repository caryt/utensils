"""Money
========

.. inheritance-diagram:: Utilities.Money
"""
from Quantity 							import Float_Quantity, Unit

class Currency(Float_Quantity):
	"""Currency is a :class:`.Float_Quantity` with units of `Money` and a currency symbol. sub-Classed to a specific currency."""
	units 	                        	= Unit('Money', symbol='?')
	separator							= ','
	digits                              = 2
	def __new__(cls, value, digits=None):
				return Float_Quantity.__new__(cls, round(value, digits or cls.digits))
	def __str__(self): 					return self._format(self.digits).format(float(self))
	def __format__(self, spec):			return self.format_rate(self, spec) or self.format_b(self, spec) or format(str(self), spec.replace('b', ''))
	def __repr__(self): 				return '{}({})'.format(self.Class.__name__, str(self))
	def __hash__(self): 				return hash(float(self))
	def __mul__(self, other):			return self.Class(float(self) * float(other))
	#def __div__(self, other):			return self.Class(float(self) / float(other))
	#def __mod__(self, other):			return self.Class(float(self) % float(other))
	def __add__(self, other):			return self.Class(float(self) + float(other))
	def __sub__(self, other):			return self.Class(float(self) - float(other))
	def __abs__(self):					return self if float(self) > 0.0 else self * -1.0
	def __eq__(self, other):			return repr(self) == repr(other)
	__rmul__ = __mul__
	# def __rdiv__(self, other):	TODO
	#	if isinstance(other, Number): 	return self.Class(float(other)/ float(self))  # Division isn't commutative
	#def __rmod__(self, other):			return self.Class(float(other)% float(self))  # Modulus isn't commutative
	__radd__ = __add__
	__rsub__ = __sub__
	def conversion(self, units):		return ''  # This is where the format spec /rate is handled for Currency objects.
	@property
	def symbol(self):					return self.units.symbol
	@property
	def Class(self):					return self.__class__

	def _format(self, digits=digits):
		"""Return a format spec to display a Currency: `?{:0.2f}`, e.g. $10.00."""
		return '{C}{{:0{S}.{D}f}}'.format(C=self.units.symbol, S=self.separator, D=digits or self.digits)  # i.e. '?{:0,.2f}''
	@property
	def _format_k(self):
		"""Return a format spec to display a Currency in kilo-dollars, e.g. $10k."""
		return '{C}{{:0{S}.{D}f}}k'.format(C=self.units.symbol, S=self.separator, D=0)  # i.e. '?{:0,.0f}k''

	@classmethod
	def fromString(cls, string):
		string 						= string.strip(cls.units.symbol).replace(cls.separator, '')
		return cls(float(string))

	#TODO - toWords (useful for cheques!)

class Dollars(Currency):
	"""A Currency in dollars and cents."""
	units 	                    	    = Unit('dollars', symbol='$')
	@property
	def dollars(self):
		"""Return the dollars only."""
		return self.Class(self // 1.0)

	@property
	def round_dollars(self):
		"""Return the dollars only, rounded to the nearest dollar."""
		return self.Class((self + 0.5) // 1.0)

	@property
	def round_cents(self):
		"""Return the amount, rounded to the nearest cent."""
		return self.Class(self, self.digits)

	@property
	def cents(self):
		"""Return the cents only."""
		return Cents(self % 1.0 * 100)

	@property
	def asCents(self):
		"""Return the amount as an integer number of cents."""
		return int(self * 100)

	@property
	def toWords(self):
		"""Return the dollars value spelt out in words as *x dollars and y cents*."""
		return self.conj(Dollars(self.dollars)._toWords(), self.cents.toWords)


	#def coinage(self):....

class Cents(Dollars):
	"""A Currency for cents only, displayed as, e.g. *5c*."""
	units 	                    	    = Unit('cents', symbol='c')
	def __new__(cls, cents): 			return Currency.__new__(cls, cents / 100.0)
	def __str__(self): 					return '{:.0f}{}'.format(float(self) * 100, self.symbol)
	@property
	def toWords(self):					return self.xillions(self * 10000, 0) if self else ''
