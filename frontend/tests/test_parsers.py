from frontend.parsers import *

route_segment_data = {'points': [{'id': 3, 'name': 'Rysy', 'x': 49.17953, 'y': 20.08806},
                                 {'id': 4, 'name': 'Czarny Staw nad Morskim Okiem', 'x': 49.18827, 'y': 20.07542},
                                 {'id': 5, 'name': 'Schronisko PTTK nad Morskim Okiem', 'x': 49.201401, 'y': 20.070999},
                                 {'id': 6, 'name': 'Wodogrzmoty Mickiewicza', 'x': 49.23422, 'y': 20.08704},
                                 {'id': 7, 'name': 'Palenica Białczańska', 'x': 49.25501, 'y': 20.10297}],
                      'segments': [{'distance': 2900, 'height_diff_down': 70, 'height_diff_up': 986, 'id': 5,
                                    'name': 'Czarny Staw nad Morskim Okiem - Rysy', 'point_1': 4, 'point_2': 3, 'region': 1, 'score': 13,
                                    'score_reverse': 4}, {'distance': 1800, 'height_diff_down': 59, 'height_diff_up': 236, 'id': 6,
                                    'name': 'Schronisko PTTK nad Morskim Okiem - Czarny Staw nad Morskim Okiem',
                                    'point_1': 5, 'point_2': 4, 'region': 1, 'score': 4, 'score_reverse': 2},
                                    {'distance': 4900, 'height_diff_down': 367, 'height_diff_up': 61, 'id': 7,
                                    'name': 'Schronisko PTTK nad Morskim Okiem - Wodogrzmoty Mickiewicza', 'point_1': 5, 'point_2': 6, 'region': 1,
                                    'score': 5, 'score_reverse': 8}, {'distance': 2800, 'height_diff_down': 132, 'height_diff_up': 16, 'id': 8,
                                    'name': 'Wodogrzmoty Mickiewicza - Palenica Białczańska', 'point_1': 6,
                                    'point_2': 7, 'region': 1, 'score': 3, 'score_reverse': 4}]}


route_data = {'got_id': None, 'id': '50', 'name': 'Ultymatywna trasa', 'score': 29, 'segments': [{'direction': False, 'segment': {'distance': 2800, 'height_diff_down': 132, 'height_diff_up': 16, 'id': 8, 'name': 'Wodogrzmoty Mickiewicza - Palenica Białczańska', 'point_1': {'id': 6, 'name': 'Wodogrzmoty Mickiewicza', 'x': 49.23422, 'y': 20.08704}, 'point_2': {'id': 7, 'name': 'Palenica Białczańska', 'x': 49.25501, 'y': 20.10297}, 'region': 1, 'score': 3, 'score_reverse': 4}}, {'direction': False, 'segment': {'distance': 4900, 'height_diff_down': 367, 'height_diff_up': 61, 'id': 7, 'name': 'Schronisko PTTK nad Morskim Okiem - Wodogrzmoty Mickiewicza', 'point_1': {'id': 5, 'name': 'Schronisko PTTK nad Morskim Okiem', 'x': 49.201401, 'y': 20.070999}, 'point_2': {'id': 6, 'name': 'Wodogrzmoty Mickiewicza', 'x': 49.23422, 'y': 20.08704}, 'region': 1, 'score': 5, 'score_reverse': 8}}, {'direction': True, 'segment': {'distance': 1800, 'height_diff_down': 59, 'height_diff_up': 236, 'id': 6, 'name': 'Schronisko PTTK nad Morskim Okiem - Czarny Staw nad Morskim Okiem', 'point_1': {'id': 5, 'name': 'Schronisko PTTK nad Morskim Okiem', 'x': 49.201401, 'y': 20.070999}, 'point_2': {'id': 4, 'name': 'Czarny Staw nad Morskim Okiem', 'x': 49.18827, 'y': 20.07542}, 'region': 1, 'score': 4, 'score_reverse': 2}}, {'direction': True, 'segment': {'distance': 2900, 'height_diff_down': 70, 'height_diff_up': 986, 'id': 5, 'name': 'Czarny Staw nad Morskim Okiem - Rysy', 'point_1': {'id': 4, 'name': 'Czarny Staw nad Morskim Okiem', 'x': 49.18827, 'y': 20.07542}, 'point_2': {'id': 3, 'name': 'Rysy', 'x': 49.17953, 'y': 20.08806}, 'region': 1, 'score': 13, 'score_reverse': 4}}], 'status': None, 'tourist_id': 1, 'verification_date': None}


def test_parse_data_for_browser():
    expected_names = ['Rysy', 'Czarny Staw nad Morskim Okiem', 'Schronisko PTTK nad Morskim Okiem',
                      'Wodogrzmoty Mickiewicza', 'Palenica Białczańska', 'Czarny Staw nad Morskim Okiem - Rysy',
                      'Schronisko PTTK nad Morskim Okiem - Czarny Staw nad Morskim Okiem',
                      'Schronisko PTTK nad Morskim Okiem - Wodogrzmoty Mickiewicza',
                      'Wodogrzmoty Mickiewicza - Palenica Białczańska']

    expected_id_mapping = {
        'points': {'Rysy': 3, 'Czarny Staw nad Morskim Okiem': 4, 'Schronisko PTTK nad Morskim Okiem': 5,
                   'Wodogrzmoty Mickiewicza': 6, 'Palenica Białczańska': 7},
        'segments': {'Czarny Staw nad Morskim Okiem - Rysy': 5,
                     'Schronisko PTTK nad Morskim Okiem - Czarny Staw nad Morskim Okiem': 6,
                     'Schronisko PTTK nad Morskim Okiem - Wodogrzmoty Mickiewicza': 7,
                     'Wodogrzmoty Mickiewicza - Palenica Białczańska': 8}}

    names, mapping = parse_data_for_browser(route_segment_data)

    assert names == expected_names
    assert mapping == expected_id_mapping


def test_parse_data_for_browser_null():
    data = {}
    expected_names = []
    expected_id_mapping = {'points': {}, 'segments': {}}

    names, mapping = parse_data_for_browser(data)

    assert names == expected_names
    assert mapping == expected_id_mapping


def test_get_element_by_id():
    data = route_segment_data['points']
    id = 7
    expected_element = {'id': 7, 'name': 'Palenica Białczańska', 'x': 49.25501, 'y': 20.10297}

    element = get_element_by_id(id, data)

    assert element == expected_element


def test_get_element_by_id_null():
    data = route_segment_data['points']
    id = 77
    expected_element = {}

    element = get_element_by_id(id, data)

    assert element == expected_element


def test_get_correlated_segments():
    point_id = 7
    data = route_segment_data['segments']

    expected_segments = [{'distance': 2800, 'height_diff_down': 132, 'height_diff_up': 16, 'id': 8,
                          'name': 'Wodogrzmoty Mickiewicza - Palenica Białczańska', 'point_1': 6,
                          'point_2': 7, 'region': 1, 'score': 3, 'score_reverse': 4}]

    correlated = get_correlated_segments(point_id, data)

    assert expected_segments == correlated


def test_get_correlated_segments_bad_point_id():
    point_id = "I'm a string BUHAHAHAHAHAH"
    data = route_segment_data['segments']

    expected_segments = []

    correlated = get_correlated_segments(point_id, data)

    assert expected_segments == correlated


def test_get_correlated_segments_no_segments():
    point_id = 7
    data = []

    expected_segments = []

    correlated = get_correlated_segments(point_id, data)

    assert expected_segments == correlated


def test_get_route_points():
    route = route_data
    expected_points = [{'id': 6, 'name': 'Wodogrzmoty Mickiewicza', 'x': 49.23422, 'y': 20.08704},
                       {'id': 5, 'name': 'Schronisko PTTK nad Morskim Okiem', 'x': 49.201401, 'y': 20.070999},
                       {'id': 4, 'name': 'Czarny Staw nad Morskim Okiem', 'x': 49.18827, 'y': 20.07542},
                       {'id': 7, 'name': 'Palenica Białczańska', 'x': 49.25501, 'y': 20.10297},
                       {'id': 3, 'name': 'Rysy', 'x': 49.17953, 'y': 20.08806}]

    points = get_route_points(route)

    assert points == expected_points


def test_get_route_points_null():
    route = {}
    expected_points = []

    points = get_route_points(route)

    assert points == expected_points
