"""Date
=======

.. inheritance-diagram:: Utilities.Date
"""
#TODO - dayfirst should be in Locale
from Utilities.DateParser 				import parse
import time


class classproperty(property):
	def __get__(self, cls, owner):
		return self.fget.__get__(None, owner)()


class Weekday(int):
	"""An enumerated type for days of the week (Sun..Sat)"""
	__slots__ = ()
	_Weekday  = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
	def __str__(self): 			return self._Weekday[self][:3]
	def __repr__(self): 		return 'Weekday(%s)' % self


#Define variable names for each weekday (Sun..Sat)
Sun, Mon, Tue, Wed, Thu, Fri, Sat 	= (Weekday(d) for d in range(0, 7))
Weekend 							= [Sat, Sun]


class Date(object):
	"""An idealised date (year, month, day).

	d = Date(2013,Jan,1) returns a date representing 1-Jan-2013
	Date Literals are supported in program source too, e.g. 1-Jan-2013 (!)
	d.year  returns a Date object representing the Year (e.g. 2013)
	d.month returns a Date object representing the month and Year (e.g. Jan-2013)
	d.day   returns a Date object representing the date, i.e. itself (e.g. 1-Jan-2013)
	d.weekday, d.week, d.ymd, d.inLeapYear()
	int(d) returns the Julian day number, Date(n) returns a Date from julian day number n
	"""
	__slots__ 	= ('y', 'm', 'd')
	def __init__(self, y, m=None, d=None):
		if m is None and d is None: return self._toDate(y)
		self.ymd = (y, m, d)
		if d> len(self.month): raise OverflowError, "Day is past end of month"

	@classproperty
	@classmethod
	def today(self):
		now = time.localtime()
		return Date(now[0], now[1], now[2])

	@classproperty
	@classmethod
	def tomorrow(self):  		return Date.today + 1*days

	@classproperty
	@classmethod
	def yesterday(self): 		return Date.today - 1*days

	@classmethod
	def fromString(self, string):
		date 					= parse(string, dayfirst=True).date()
		return Date(date.year, date.month, date.day)

	@property
	def day(self): 		 		return self
	@property
	def month(self): 	 		return Month(self.y, self.m)
	@property
	def year(self): 	 		return Year(self.y)
	@property
	def weekday(self):	 		return Weekday(int(self) % 7)
	@property
	def week(self):		 		return Week(Date(int(self) - self.weekday))
	@property
	def ymd(self): 		 		return (self.y, self.m, self.d)
	@ymd.setter
	def ymd(self, value):		self.y, self.m, self.d = value
	@property
	def timetuple(self):		return self.ymd + (0, 0, 0, 0, 0, 0)

	def __repr__(self):  		return str(self)
	def __len__(self): 			return len(self.month)  if self.d == 0 else 1
	def __iter__(self): 		return iter(self.month) if self.d == 0 else None
	def __contains__(self, d):	return d in self.month  if self.d == 0 else (d == self.d)
	def __getstate__(self):		return self.ymd
	def __setstate__(self, s):	self.ymd = s
	def __eq__(self, d): 		return (self.ymd == d.ymd)
	def __ne__(self, d): 		return (self.ymd != d.ymd)
	def __lt__(self, d): 		return (self.ymd  < d.ymd)
	def __le__(self, d):		return (self.ymd <= d.ymd)
	def __gt__(self, d): 		return (self.ymd  > d.ymd)
	def __ge__(self, d): 		return (self.ymd >= d.ymd)
	def inLeapYear(self):		return (self.y % 4 == 0) and ((self.y % 100 !=0) or (self.y % 400 == 0))
	def _hyphenate(self, a, b):	return '%s%s%s' % (a, '-' if a and b else '', b)
	def __str__(self): 			return self._hyphenate(self.d if self.d else '', str(self.month))
	def __add__(self, n): 		return Date(int(self) + n) if n != 0 else self
	def __hash__(self):			return hash((self.y, self.m, self.d))
	def __format__(self, spec):
		"""Allow strftime formatting e.g. format(date, '%d%m%y:6')."""
		#TODO - This assumes a :, doesn't allow "!%d" or "!%d:6", just "%d:".
		time_spec, fmt_spec 	= spec.split(':') if ':' in spec else (spec, '')
		formatted				= time.strftime(time_spec, self.timetuple) if time_spec != '' else None
		return format(str(self) if formatted is None else formatted, fmt_spec)
	def __getitem__(self, item):
		if isinstance(item, Weekday) and self.d==0 and self.m!=0 and self.y!=0:
			return [d for d in self if d.weekday==item]
		return self.month[item] if self.d==0 else None

	def __int__(self):
		from datetime import date
		return date(self.y, self.m, self.d).toordinal()
	# 	#see http://www.hermetic.ch/cal_stud/jdn.htm
	# 	o = ( self.m - 14 ) // 12
	# 	return (( 1461 * (   self.y + 4800 +   o ) ) //   4 +
	# 			(  367 * (   self.m - 2 - 12 * o ) ) //  12 -
	# 			(    3 * ( ( self.y + 4900 +   o )   // 100 ) ) // 4 +
	# 			self.d - 32075 )

	def _toDate(self, jd):
		from datetime import date
		d = date.fromordinal(jd)
		self.ymd = (d.year, d.month, d.day)
	# 	#see http://www.hermetic.ch/cal_stud/jdn.htm
	# 	l = jd + 68568
	# 	n = ( 4 * l ) // 146097
	# 	l = l - ( 146097 * n + 3 ) // 4
	# 	i = ( 4000 * ( l + 1 ) ) // 1461001
	# 	l = l - ( 1461 * i ) // 4 + 31
	# 	j = ( 80 * l ) // 2447
	# 	d = l - ( 2447 * j ) // 80
	# 	l = j // 11
	# 	m = j + 2 - ( 12 * l )
	# 	y = 100 * ( n - 49 ) + i + l
	# 	self.ymd = (y, m, d)

	def __sub__(self, other):
		if isinstance(other, Date):					return DateInterval(other, self)
		#Hack for Date Literals in program source code
		if isinstance(other, int) and self.y==0: 	return Date(other, self.m, self.d)
		return Date(int(self) - other) if other != 0 else self


class Month(Date):
	"""A Date object representing just a Month and, optionally, a Year.

	List operations, e.g. Jan-2013[1], [-1], for d in Jan-2013, len(Jan-2013)
	29 in Feb-2013
	"""
	__slots__ = ()
	_Month = (	'January', 'February', 'March',
				'April',   'May',      'June',
				'July',    'August',   'September',
				'October', 'November', 'December',
			)

	_mlen  = (	31, 28, 31,
				30, 31, 30,
				31, 31, 30,
				31, 30, 31,
			)
	def __init__(self, y, m, d=0): 		self.ymd = (y, m, d)
	def __getitem__(self, item): 		return Date(self.y, self.m, item + (len(self.month)+1 if item<0 else 0))
	def __contains__(self, d): 			return (0 < d <= len(self)) if self.m != 0 else False
	def __str__(self): 					return self._hyphenate(self._Month[self.m-1][:3] if self.m else '', str(self.year))
	def __add__(self, n): 				return Month((self.m+n-1)//12, ((self.m + n-1) % 12) +1, 0)
	def __iter__(self): 				return (Date(self.y, self.m, d+1) for d in range(0, len(self.month)))

	def __len__(self):
		if self.m == 0: return len(self.year)
		return self._mlen[self.m-1] + (1 if self.m == 2 and self.inLeapYear() else 0)

	#Hacks for Date Literals in program source code
	def __rsub__(self, d):
		if isinstance(d, int) and self.d==0: return Date(self.y, self.m, d)

Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec = (Month(0, m) for m in range(1, 13))


class Year(Date):
	"""A Date object representing just a Year.

	List operations, e.g. for d in Year(2013), len(Year(2013)
	"""
	__slots__ = ()
	def __init__(self, y): 	self.ymd = (y, 0, 0)
	def __str__(self): 		return ('%4d' % self.y) if self.y else ''
	def __len__(self): 		return 365 + (1 if self.inLeapYear() else 0)
	def __add__(self, n):	return Year(self.y+n)
	def __iter__(self): 	return (d for m in range(0, 12) for d in Date(self.y, m+1, 0))


class Duration(Date):
	"""Represents a duration (days, months and years).

	Add / Subtract durations from Dates, e.g. 1-Jan-2013 + 3*years + 2*months + 15*days
	"""
	__slots__ = ()
	def __init__(self, y, m, d): 	self.ymd = (y+int(m/12), m%12, d)

	def __str__(self):
		days 						= '%d %s ' % (self.d, _.plural(self.d, 'day'))   if self.d else ''
		months 						= '%d %s ' % (self.m, _.plural(self.m, 'month')) if self.m else ''
		years  						= '%d %s ' % (self.y, _.plural(self.y, 'year'))  if self.y else ''
		return ('%s%s%s' % (years, months, days)).strip()

	def __len__(self): 				return 'Not implemented'
	def __mul__(self, n): 			return Duration(self.y*n, self.m*n, self.d*n)
	def __rmul__(self, n): 			return Duration(self.y*n, self.m*n, self.d*n)
	def __add__(self, d):
		if isinstance(d, Duration):
			return Duration(self.y+d.y, self.m+d.m, self.d+d.d)
	def __getitem__(self, item): 	return None

	def __radd__(self, d):
		if not isinstance(d, Date): raise TypeError
		#print d, 'plus', self.y, self.m, self.d,
		yy 		= d.year    	+ self.y
		mm 		= d.month 		+ self.m
		dd      = min(len(Month(yy.y + mm.y, mm.m)), d.d)
		result 	= Date(yy.y + mm.y, mm.m, dd) + self.d
		return result

	def __rsub__(self, d):
		if not isinstance(d, Date): raise TypeError
		return d + Duration(self.y * -1, self.m * -1, self.d * -1)
	@property
	def duration(self):				return self
	@property
	def months(self):
		"""Return the total number of years and months, in whole months (ignoring any days)."""
		return self.y * 12 + self.m


class _Days(int):
	"""A Duration representing a number of days"""
	def __rmul__(self, d): return Duration(y=0, m=0, d=d)


class _Months(int):
	"""A Duration representing a number of months"""
	def __rmul__(self, m): return Duration(y=0, m=m, d=0)


class _Years(int):
	"""A Duration representing a number of years"""
	def __rmul__(self, y): return Duration(y=y, m=0, d=0)


#These variables allow nice duration expressions, e.g. d = 3*years + 2*months + 15*days
days, months, years = _Days(), _Months(), _Years()


class Interval(object):
	"""An Interval representing a list from start to end, [start..end].

	Suitable base class for Date Intervals
	i = Interval(start,end) returns the Interval starting at start and continuing to end (inclusive)
	Usage examples: i[0], i[-1], len(i), for x in i, x in i.
	Requires definitions for i+1, i<=j, i-j
	Note that either start or end may be None, indicating an open interval.
	"""
	__slots__ = ('_start', '_end')
	def __init__(self, start, end): 	self._start, self._end = (start, end)
	def __str__(self): 					return '[%s..%s]' % (self._start, self._end)
	def __repr__(self):					return '%s(%s,%s)' % (self.__class__.__name__, self._start, self._end)
	def __len__(self):					return abs(int(self._end) - int(self._start))
	def __eq__(self, other):			return (self._start, self._end) == (other._start, other._end)
	def __contains__(self, i):
		##Note that if start==None or end==None are handled here
		if self._start is None and self._end is None: return (i is None)
		return 	((self._start <= i)		if self._start is not None else True) and \
				((i <= self._end)		if self._end   is not None else True)
	def max_start(self, other):
		return max(self._start, other._start) if self._start is not None else other._start
	def min_end(self, other):
		return min(self._end, other._end) if self._end is not None else other._end
	def __and__(self, other):
		"""Return the intersection of two Intervals (may be None)."""
		latest_start 					= self.max_start(other)
		earliest_end 					= self.min_end(other)
		if latest_start <= earliest_end:
			return Interval(latest_start, earliest_end)
		return None
	def __getitem__(self, item):
		if abs(item) > len(self): raise IndexError
		return (self._start + item + (len(self)+1 if item<0 else 0))


class DateInterval(Interval):
	@property
	def duration(self):
		if not hasattr(self, '_duration'):
			overflow_m					= (self._start.m > self._end.m)
			yy 							= self._end.y - self._start.y - ( 1 if overflow_m else 0)
			mm 							= self._end.m - self._start.m + (12 if overflow_m else 0)
			overflow_d					= (self._start.d > self._end.d)
			mm 							= mm - (1 if overflow_d else 0)
			dd 							= self._end.d - self._start.d + (len((self._end.month[1]-1).month) if overflow_d else 0)
			self._duration = Duration(	yy, mm, dd)
		return self._duration
	@property
	def d(self):			return self.duration.d
	@property
	def m(self):			return self.duration.m
	@property
	def y(self):			return self.duration.y
	@property
	def days(self):			return Duration(0, 0, len(self))
	@property
	def months(self):		return Duration(0, self.duration.y * 12 + self.duration.m, self.duration.d)
	@property
	def years(self):		return self.duration


class Week(DateInterval):
		def __init__(self, start): super(DateInterval, self).__init__(start, start+6)
