"""Date tests.

"""
from unittest import TestCase
from date import *


class Test_Weekday(TestCase):
    """Weekdays enumerate Sun..Sat."""

    def test_weekday(self):
        d = 15-Jan-2013
        self.assertEqual(d.weekday,       Tue)
        self.assertEqual(str(d.weekday), 'Tue')


class Test_Date(TestCase):
    """Date objects handle date literals and arithemtic."""

    def test_Date(self):
        d = Date(2013, 1, 15)
        self.assertEqual( str(d), '15-Jan-2013')

    def test_DateLiteral(self):
        d = 15-Jan-2013
        self.assertEqual( str(d), '15-Jan-2013')

    def test_DateString(self):
        self.assertEqual( str(15-Jan-2013), '15-Jan-2013')
        self.assertEqual( str(Jan-2013),    'Jan-2013')
        self.assertEqual( str(15-Jan),      '15-Jan')
        self.assertEqual( str( Jan),        'Jan')

    def test_invalidDate(self):
        self.assertRaises(OverflowError, lambda: 32-Jan-2013)
        self.assertRaises(OverflowError, lambda: 29-Feb-2013)

    def test_DateComponents(self):
        d = 15-Jan-2013
        self.assertEqual(d.day,   Date(2013, 1, 15))
        self.assertEqual(d.month, Date(2013, 1, 0))
        self.assertEqual(d.month, Month(2013, 1))
        self.assertEqual(d.year,  Date(2013, 0, 0))
        self.assertEqual(d.year,  Year(2013))
        self.assertEqual(d.ymd,   (2013, 1, 15))

    def test_month_items(self):
        m = Feb-2013
        self.assertEqual(m[ 1],  1-Feb-2013)
        self.assertEqual(m[-1], 28-Feb-2013)
        m = Mar-2013
        self.assertEqual(m[ 1],  1-Mar-2013)
        self.assertEqual(m[-1], 31-Mar-2013)
        d = 15-Mar-2013
        self.assertEqual(d.month[ 1],  1-Mar-2013)
        self.assertEqual(d.month[-1], 31-Mar-2013)

    def test_month(self):
        [self.assertEqual(date, Date(2013, 1, d + 1))
            for (d, date) in enumerate(Jan-2013)]

    def test_julian(self):
        #self.assertEqual(int(1-Jan-2013), 2456295)
        self.assertEqual(Date(int(31-Jan-2013) + 1), 1-Feb-2013)
        self.assertEqual(Date(int(31-Jan-2013)),    31-Jan-2013)

    def test_year(self):
        j = int(1-Jan-2013)
        for date in Year(2013):
            self.assertEqual(date,      Date(j))
            self.assertEqual(int(date), j)
            j += 1

    def test_week(self):
        w = (15-Jan-2013).week
        self.assertEqual(w[0],   13-Jan-2013)
        self.assertEqual(w[Sun], 13-Jan-2013)
        self.assertEqual(w[-1],  19-Jan-2013)
        self.assertEqual(w[Sat], 19-Jan-2013)
        self.assertEqual(str(w), '[13-Jan-2013..19-Jan-2013]')
        self.assertFalse(12-Jan-2013 in w)
        self.assertTrue( 13-Jan-2013 in w)
        self.assertTrue( 14-Jan-2013 in w)
        self.assertTrue( 19-Jan-2013 in w)
        self.assertFalse(20-Jan-2013 in w)

    def test_day_in_date(self):
        self.assertTrue(  1 in Jan-2013)
        self.assertTrue( 31 in Jan-2013)
        self.assertTrue(  1 in Feb-2013)
        self.assertFalse(31 in Feb-2013)
        self.assertTrue( 28 in Feb-2013)
        self.assertFalse(29 in Feb-2013)
        self.assertTrue( 29 in Feb-2012)

    def test_rawAddition(self):
        self.assertEqual(31-Jan-2013 + 1,        1-Feb-2013)

    def test_yesterday_today_tomorrow(self):
        self.assertEqual(int(Date.yesterday+1), int(Date.today))
        self.assertEqual(int(Date.tomorrow -1), int(Date.today))


    def test_format(self):
        """format(date, spec) allows strftime specs, e.g. format(date, '%d%m%y:6')."""
        self.assertEqual(format(1-Mar-2013, '%d%m%y:6'), '010313')
        self.assertEqual(format(1-Mar-2013, '%Y%m%d:8'), '20130301')

class Test_Month(TestCase):
    """Month objects represent a Month and Year."""

    def test_month_lengths(self):
        self.assertEqual(len(Feb-1900), 28)
        self.assertEqual(len(Feb-1901), 28)
        self.assertEqual(len(Feb-1902), 28)
        self.assertEqual(len(Feb-1903), 28)
        self.assertEqual(len(Feb-1904), 29)
        self.assertEqual(len(Feb-2000), 29)
        self.assertEqual(len(Feb-2001), 28)
        self.assertEqual(len(Feb-2002), 28)
        self.assertEqual(len(Feb-2003), 28)
        self.assertEqual(len(Feb-2004), 29)


class Test_Year(TestCase):
    """Year objects represent a Year."""

    def test_year_lengths(self):
        self.assertEqual(len((Feb-1900).year), 365)
        self.assertEqual(len((Feb-1901).year), 365)
        self.assertEqual(len((Feb-1902).year), 365)
        self.assertEqual(len((Feb-1903).year), 365)
        self.assertEqual(len((Feb-1904).year), 366)
        self.assertEqual(len((Feb-2000).year), 366)
        self.assertEqual(len((Feb-2001).year), 365)
        self.assertEqual(len((Feb-2002).year), 365)
        self.assertEqual(len((Feb-2003).year), 365)
        self.assertEqual(len((Feb-2004).year), 366)


class Test_Duration(TestCase):
    """Durations are a number of days, months and/or years."""

    def test_Duration(self):
        self.assertEqual(str(7*days),   '7 days')
        self.assertEqual(str(2*months), '2 months')
        self.assertEqual(str(3*years),  '3 years')
        self.assertEqual(31-Dec-2012 + 1*days,    1-Jan-2013)
        self.assertEqual(31-Dec-2012 + 1*months, 31-Jan-2013)
        self.assertEqual(31-Dec-2012 + 2*months, 28-Feb-2013)
        self.assertEqual(28-Feb-2013 - 2*months, 28-Dec-2012)  # TODO: Is this right?
        self.assertEqual(31-Mar-2013 + 1*months, 30-Apr-2013)
        self.assertEqual(15-Jan-2013 + 7*days,   22-Jan-2013)
        self.assertEqual(15-Jan-2013 + 3*months, 15-Apr-2013)
        self.assertEqual(15-Jan-2013 + 2*years,  15-Jan-2015)
        d = 2*years + 3*months + 15*days
        self.assertEqual(d,      Duration(2, 3, 15))
        self.assertEqual(str(d), '2 years 3 months 15 days')
        self.assertEqual(1-Jan-2013 + 15*days,   16-Jan-2013)
        self.assertEqual(1-Apr-2013 + 15*days,   16-Apr-2013)
        self.assertEqual(1-Jan-2013 + d,         16-Apr-2015)
        self.assertEqual(16-Apr-2013- d,          1-Jan-2011)


class Test_DateInterval(TestCase):
    """Date Intervals are [start..end]."""

    def test_DateInterval_1(self):
        i = (16-Apr-2015) - (1-Jan-2013)
        self.assertEqual(str(i),                '[1-Jan-2013..16-Apr-2015]')
        self.assertEqual(i.d,                   15)
        self.assertEqual(i.m,                   3)
        self.assertEqual(i.y,                   2)
        self.assertEqual(i.days,                835 * days)
        self.assertEqual(i.months,          27 * months + 15 * days)
        self.assertEqual(i.years,               2 * years + 3 * months + 15 * days)
        self.assertEqual(i.duration,            Duration(2, 3, 15))
        self.assertEqual(len(i),                835)
        self.assertTrue( 16-Apr-2015 in i)
        self.assertTrue(  1-Jan-2013 in i)
        self.assertFalse(17-Apr-2015 in i)
        self.assertFalse(31-Dec-2012 in i)

    def test_DateInterval_2(self):
        i = (1-Jan-2013) - (7-Dec-1963)
        self.assertEqual(len(i),                17923)
        self.assertEqual(i.years,               49 * years + 25 * days)

    def test_DateInterval_3(self):
        i = (1-Mar-2013) - (28-Feb-2013)
        self.assertEqual(len(i),                1)
        self.assertEqual(i.years,               1 * days)

    def test_DateInterval_4(self):
        i = (1-Mar-2012) - (28-Feb-2012)
        self.assertEqual(len(i),                2)
        self.assertEqual(i.years,               2 * days)

    def test_DateInterval_5(self):
        i = (31-Mar-2012) - (1-Mar-2012)
        self.assertEqual(len(i),                30)
        self.assertEqual(i.years,               30 * days)

    def test_DateInterval_fromNone(self):
        i = DateInterval(None, 1-Jan-2013)
        self.assertTrue(  1-Jan-2013 in i)
        self.assertFalse( 2-Jan-2013 in i)

    def test_DateInterval_toNone(self):
        i = DateInterval( 1-Jan-2013, None)
        self.assertFalse(31-Dec-2012 in i)
        self.assertTrue(  1-Jan-2013 in i)

    def test_DateInterval_allNone(self):
        i = DateInterval( None, None)
        self.assertFalse(31-Dec-2012 in i)
        self.assertFalse( 1-Jan-2013 in i)
        self.assertTrue(None in i)

    def test_DateInterval_intersection(self):
        i = DateInterval( 1-Mar-2012, 31-Mar-2012)
        self.assertEqual(i & DateInterval( 1-Jan-2012, 31-Dec-2012), i)
        self.assertEqual(i & DateInterval( 1-Jan-2012, 15-Mar-2012), DateInterval( 1-Mar-2012, 15-Mar-2012))
        self.assertEqual(i & DateInterval(15-Mar-2012, 20-Mar-2012), DateInterval(15-Mar-2012, 20-Mar-2012))
        self.assertEqual(i & DateInterval( 1-Apr-2012,  1-May-2012), None)

class Test_Week(TestCase):
    """Week objects are DateIntervals that represent a calendar week [Sun..Sat]."""

    def test_week2(self):
        d = 15-Jan-2013
        self.assertEqual(d.week[Fri], 18-Jan-2013)
        self.assertEqual(d.week[Mon], 14-Jan-2013)
        d = Jan-2013
        self.assertEqual(d[Fri], [4-Jan-2013, 11-Jan-2013, 18-Jan-2013, 25-Jan-2013])
        self.assertEqual(d[Fri][-1], 25-Jan-2013)

