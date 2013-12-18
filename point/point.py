# -*- coding: utf-8 -*-
"""Points, Angles and Geographical Coordinates
==============================================
"""
from math import radians, degrees, cos, sin, sqrt, pow, atan2


class Point(tuple):
    """A Point in space (x, y, z)."""
    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @property
    def radius(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    @property
    def theta(self):
        return Angle.fromRadians(atan2(self.y, self.x))

    def __len__(self):
        return self.radius


class Angle(float):
    """An Angle (in degrees) - a float with some extra methods."""
    @classmethod
    def fromRadians(cls, radians):
        return cls(degrees(radians))

    @property
    def radians(self):
        """Return the Angle in Radians."""
        return radians(self)

    @property
    def cos(self):
        """Return the cosine of the Angle."""
        return cos(radians(self))

    @property
    def sin(self):
        """Return the sine of the Angle."""
        return sin(radians(self))

    @property
    def degrees(self):
        """Return the whole number of Degrees in the Angle."""
        return int(self)

    @property
    def minutes(self):
        """Return the whole number of Minutes in the Angle."""
        return int((self - self.degrees) / 60)

    @property
    def seconds(self):
        """Return the number of Seconds in the Angle."""
        return 0

    def __str__(self):
        return "%d° %d′ %d″" % (self.degrees, self.minutes, self.seconds)
        # return "%do %d' %d%s" % (self.degrees, self.minutes, self.seconds, '"')


class Coordinate(Point):
    """Geographical Coordinate (Latitude, Longitude and Elevation).
    """
    def __new__(self, (lat, lng, ele)):
        return Point.__new__(self, (Angle(lat), Angle(lng), ele))

    @property
    def latitude(self):
        """Return the Latitude."""
        return self[0]

    @property
    def longitude(self):
        """Return the Longitude."""
        return self[1]

    @property
    def elevation(self):
        """Return the Elevation."""
        return self[2]

    @property
    def northern(self):
        """Return True if this is in the northern hemisphere."""
        return (self.latitude >= 0)

    def __str__(self):
        return "(%s, %s, %sm)" % (self.latitude, self.longitude, self.elevation)
