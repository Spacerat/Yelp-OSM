import math

EARTH_EQUITORIAL_RADIUS = 6378137.0
EARTH_POLAR_RADIUS = 6356752.3

def geocentric_radius(lattitude, equitorial_radius=EARTH_EQUITORIAL_RADIUS, polar_radius=EARTH_POLAR_RADIUS):
	""" Find the radius of a spheroid at a certain latitude """
	# https://en.wikipedia.org/wiki/Earth_radius#Location-dependent_radii
    sin_lat = math.sin(lattitude)
    cos_lat = math.cos(lattitude)
    top = ((equitorial_radius**2) * cos_lat )**2 + ((polar_radius**2) * sin_lat )**2
    bottom = (equitorial_radius * cos_lat )**2 + (polar_radius * sin_lat )**2
    return math.sqrt(top/bottom)

def degrees_to_metres(latitude, longitude, search_radius):
	""" For a given point on the earth, find the size of one degree of latitude or longitude, in metres """
	# Haversine formula
	# https://en.wikipedia.org/wiki/Haversine_formula
    radius = math.radians(search_radius)
    lat1 = math.radians(latitude)
    long1 = math.radians(longitude)
    lat2 = lat1 + radius
    long2 = long1 + radius
    sphere_radius = geocentric_radius(latitude)

    len_lat = 2 * sphere_radius * math.asin(math.sqrt(math.sin((lat2-lat1)/2)**2))
    len_long = 2 * sphere_radius * math.asin(math.sqrt((math.cos(lat1)**2)*(math.sin((long2-long1)/2)**2)))
    both = 2 * sphere_radius * math.asin(math.sqrt(math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*(math.sin((long2-long1)/2)**2)))
    return (len_lat, len_long)
