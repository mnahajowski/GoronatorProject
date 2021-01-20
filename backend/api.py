from flask import Flask, jsonify, request, make_response

from endpoints.points import points
from endpoints.routes import routes
import json

app = Flask(__name__)
ALLOWED_URLS = 'http://localhost:5000'


@app.route("/route_segments")
def index():
    all_points = points.get_points()
    all_segments = points.get_segments()
    return {"points": all_points, "segments": all_segments}


@app.route("/segments")
def segments():
    all_segments = points.get_segments()
    response = jsonify({'segments': all_segments})
    response.headers.add('Access-Control-Allow-Origin', ALLOWED_URLS)
    return response


@app.route("/segment/<segment_list>")
def segments_by_id(segment_list):
    segment_list = segment_list.split(',')
    all_segments = points.get_segments_by_ids(segment_list)

    return {"segments": all_segments}


@app.route('/point/<point_list>')
def points_by_id(point_list):
    point_list = point_list.split(',')
    all_points = points.get_points_by_id(point_list)
    response = jsonify({'points': all_points})
    response.headers.add('Access-Control-Allow-Origin', ALLOWED_URLS)
    return response


@app.route('/correlated/<point_id>')
def correlated(point_id):
    segments = points.get_correlated_segments(point_id)
    response = jsonify({'segments': segments})
    response.headers.add('Access-Control-Allow-Origin', ALLOWED_URLS)
    return response


@app.route('/new_route', methods=["POST"])
def insert_route():
    route = json.loads(request.data)

    route_id = routes.insert_new_route(route)

    response = jsonify({"status": 200, "route_id": route_id})
    response.headers.add('Access-Control-Allow-Origin', ALLOWED_URLS)
    return response


@app.route('/update_route/<route_id>', methods=["POST"])
def update_route(route_id):
    route = json.loads(request.data)

    routes.update_route(route_id, route)

    response = jsonify({"status": 200})
    response.headers.add('Access-Control-Allow-Origin', ALLOWED_URLS)
    return response


@app.route('/routes/<tourist_id>')
def route_list(tourist_id):
    all_routes = routes.get_route_names(tourist_id)
    response = jsonify({"routes": all_routes})
    response.headers.add('Access-Control-Allow-Origin', ALLOWED_URLS)
    return response


@app.route('/route/full/<route_id>')
def full_route(route_id):
    route = routes.get_full_route(route_id)
    response = jsonify(route)
    response.headers.add('Access-Control-Allow-Origin', ALLOWED_URLS)
    return response


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
