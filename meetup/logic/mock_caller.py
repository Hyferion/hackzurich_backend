from traveltime_client import get_overlap
from polygon_maths import fit_circle


def unwrap_coords(response, coords_id):
    return response['results'][coords_id]['shapes'][0]['shell']


def get_pairs(coords):
    return [[item['lng'], item['lat']] for item in coords]


def get_string(pairs):
    return '\n'.join([','.join(i) for i in pairs])


def filter_results(results, search_id):
    new_results = []
    for item in results:
        if item['search_id'] == search_id:
            new_results.append(item)
    return new_results


departure_searches = [
    {
        "id": "A",
        "coords": {
            "lat": 51.507609,
            "lng": -0.128315
        },
        "transportation": {
            "type": "public_transport"
        },
        "departure_time": "2019-09-27T08:00:00Z",
        "travel_time": 900
    },
    {
        "id": "B",
        "coords": {
            "lat": 51.510918,
            "lng": -0.117268
        },
        "transportation": {
            "type": "walking"
        },
        "departure_time": "2019-09-27T08:00:00Z",
        "travel_time": 600
    }
]

results = get_overlap(departure_searches).json()['results']
overlap = filter_results(results, 'overlap')

overlap_pairs = get_pairs(overlap[0]['shapes'][0]['shell'])

print(fit_circle(overlap_pairs))


# overlap_string = get_string(overlap_pairs)

# print('overlap')
# print(overlap_string)
