from traveltime_client import get_overlap
from gmaps_client import get_nearby_places
from polygon_maths import fit_circle


def unwrap_coords(response, coords_id):
    return response['results'][coords_id]['shapes'][0]['shell']


def get_pairs(coords):
    return [[item['lng'], item['lat']] for item in coords]


def get_string(pairs):
    return '\n'.join([','.join(i) for i in pairs])


def reverse_coord_order(coord):
    return [coord[1], coord[0]]


departure_searches = [
    {
        'id': 'A',
        'coords': {
            'lat': 51.507609,
            'lng': -0.128315
        },
        'transportation': {
            'type': 'public_transport'
        },
        'departure_time': '2019-09-27T08:00:00Z',
        'travel_time': 900
    },
    {
        'id': 'B',
        'coords': {
            'lat': 51.510918,
            'lng': -0.117268
        },
        'transportation': {
            'type': 'walking'
        },
        'departure_time': '2019-09-27T08:00:00Z',
        'travel_time': 600
    }
]

overlap_pairs = get_overlap(departure_searches)

centroid, radius = fit_circle(overlap_pairs)

print(get_nearby_places(reverse_coord_order(
    centroid), radius, 'restaurant')
