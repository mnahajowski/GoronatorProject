import os

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import parsers

import requests
import json

DEFAULT_MAP_INIT = [49.5, 20]

app = Flask(__name__)
DEBUG = True
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'images', 'storage')

app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

API_URL = 'http://localhost:5001'


@app.route("/")
def index():
    response = requests.get(API_URL + "/route_segments")
    data = json.loads(response.content)

    names, id_mapping = parsers.parse_data_for_browser(data)

    return render_template('index.html', id_mapping=id_mapping, names=names)


@app.route("/segment/<segment_id>")
def segment(segment_id):
    response = requests.get(API_URL + "/route_segments")
    data = json.loads(response.content)

    names, id_mapping = parsers.parse_data_for_browser(data)

    segment = parsers.get_element_by_id(int(segment_id), data['segments'])
    point_1, point_2 = parsers.get_element_by_id(segment['point_1'], data['points']), \
                       parsers.get_element_by_id(segment['point_2'], data['points'])

    map_init_point = ((point_1['x'] + point_2['x']) / 2, (point_1['y'] + point_2['y']) / 2)

    return render_template('route_element.html', names=names, id_mapping=id_mapping, route_element=segment,
                           points=[point_1, point_2], map_init=map_init_point)


@app.route("/point/<point_id>")
def point(point_id):
    response = requests.get(API_URL + "/route_segments")
    data = json.loads(response.content)

    names, id_mapping = parsers.parse_data_for_browser(data)
    point = parsers.get_element_by_id(int(point_id), data['points'])
    map_init_point = (point['x'], point['y'])
    correlated_segments = parsers.get_correlated_segments(int(point_id), data['segments'])

    return render_template('route_element.html', names=names, id_mapping=id_mapping, route_element=point,
                           points=[point], map_init=map_init_point, correlated_segments=correlated_segments)


@app.route("/route")
@app.route("/route/<segment_id>")
def route(segment_id=None):
    if segment_id:
        response = requests.get(API_URL + "/segment/" + segment_id)
        segment = json.loads(response.content)['segments']

        response = requests.get(f"{API_URL}/point/{segment[0]['point_1']},{segment[0]['point_2']}")
        points = json.loads(response.content)['points']
    else:
        segment = []
        points = []

    map_init = [(points[0]['x'] + points[1]['x']) / 2, (points[0]['y'] + points[1]['y']) / 2] if points else DEFAULT_MAP_INIT

    return render_template('route.html', segments=segment, points=points, map_init=map_init)


@app.route("/routes/<tourist_id>")
@app.route("/routes/<tourist_id>/<route_id>")
def routes(tourist_id, route_id=False):
    response = requests.get(API_URL + "/routes/" + tourist_id)
    routes = json.loads(response.content)['routes']

    if route_id:
        response = requests.get(API_URL + "/route/full/" + route_id)
        route = json.loads(response.content)

        if route['segments']:
            map_init = route['segments'][len(route['segments']) // 2]['segment']['point_1']['x'], \
                       route['segments'][len(route['segments']) // 2]['segment']['point_1']['y']
        else:
            map_init = DEFAULT_MAP_INIT

        points = [seg['segment']['point_1'] for seg in route['segments']] + [seg['segment']['point_2']
                                                                             for seg in route['segments']]
        ids = set()
        filtered_points = []

        for point in points:
            if point['id'] not in ids:
                ids.add(point['id'])
                filtered_points.append(point)

        segments = [{**seg['segment'], 'direction': seg['direction']} for seg in route['segments']]
        route_name = route['name']
    else:
        segments = []
        filtered_points = []
        map_init = DEFAULT_MAP_INIT
        route_name = ""

    return render_template('routes_manager.html', segments=segments, points=filtered_points, map_init=map_init,
                           routes=list(routes.items()), tourist_id=tourist_id, route_id=route_id, route_name=route_name)


@app.route("/routes/<route_id>/documentation", methods=['GET', 'POST'])
def documentation(route_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if not file.filename:
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)

    else:
        images = ['sample_img.jpg'] * 5  # get images
        routes = [("Super trasa 1", 1)] * 6  # get routes + ids
        return render_template('documentation.html', routes=routes, route_id=route_id, images=images)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
