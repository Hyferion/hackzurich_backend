from numpy import mean, maximum, sin, cos, sqrt, arcsin, radians
from numpy.linalg import norm


def haversine(coord1, coord2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    All args must be of equal length.    
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon/2.0)**2

    c = 2 * arcsin(sqrt(a))
    km = 6367 * c
    return km * 1000


def calculate_radius(coords, centroid):
    distances = [haversine(point, centroid) for point in coords]

    return mean(distances)


def fit_circle(coords):
    """
    Input: pairs of lat-long coordinates defining a polygon
    Output: centroid, radius of circle that best fits the polygon
    """
    centroid = mean(coords, axis=0)
    radius = calculate_radius(coords, centroid)
    return list(centroid), radius
