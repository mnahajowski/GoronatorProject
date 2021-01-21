def parse_data_for_browser(data):
    names = [elem['name'] for elem in data.get('points', [])] + [elem['name'] for elem in data.get('segments', [])]
    id_mapping = {'points': {elem['name']: elem['id'] for elem in data.get('points', [])},
                  'segments': {elem['name']: elem['id'] for elem in data.get('segments', [])}}

    return names, id_mapping


def get_element_by_id(id, elements):
    for elem in elements:
        if elem['id'] == id:
            return elem


def get_correlated_segments(point_id, segments):
    return [segment for segment in segments if segment['point_1'] == point_id or segment['point_2'] == point_id]


def get_route_points(route):
    points = [seg['segment']['point_1'] for seg in route['segments']] + [seg['segment']['point_2']
                                                                         for seg in route['segments']]
    ids = set()
    filtered_points = []
    for point in points:
        if point['id'] not in ids:
            ids.add(point['id'])
            filtered_points.append(point)
    return filtered_points
