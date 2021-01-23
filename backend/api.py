import os

from flask import Flask, jsonify, request, send_file, redirect
from flask_selfdoc import Autodoc

from werkzeug.utils import secure_filename

from backend.endpoints.points import points
from backend.endpoints.routes import routes
from backend.file_storage import manager

import json


app = Flask(__name__)
auto = Autodoc(app)
FRONTEND_URL = 'http://localhost:5000'


@auto.doc()
@app.route("/route_segments")
def index():
    """
    Obtain all route segments - segments and points
    :return: a json string in format {'points': [], 'segments': []}
    """
    all_points = points.get_points()
    all_segments = points.get_segments()
    return {"points": all_points, "segments": all_segments}


@app.route("/segments")
@auto.doc()
def segments():
    """
    Obtain all segments
    :return: a json string in format {"segments": []}
    """
    all_segments = points.get_segments()
    response = jsonify({'segments': all_segments})
    response.headers.add('Access-Control-Allow-Origin', FRONTEND_URL)
    return response


@app.route("/segment/<segment_list>")
@auto.doc()
def segments_by_id(segment_list):
    """
    Obtain specific segment(s) by id
    :param segment_list: string of ids, separated by commas
    :return: a json string in format {"segments": []}
    """
    segment_list = segment_list.split(',')
    all_segments = points.get_segments_by_ids(segment_list)

    return {"segments": all_segments}


@app.route('/point/<point_list>')
@auto.doc()
def points_by_id(point_list):
    """
    Obtain specific points(s) by id
    :param point_list: string of ids, separated by commas
    :return: a json string in format {"points": []}
    """
    point_list = point_list.split(',')
    all_points = points.get_points_by_id(point_list)
    response = jsonify({'points': all_points})
    response.headers.add('Access-Control-Allow-Origin', FRONTEND_URL)
    return response


@app.route('/correlated/<point_id>')
@auto.doc()
def correlated(point_id):
    """
    Obtain segments correlated with a point
    :param point_id: id of the point
    :return: A json string of correlated segments in format {"segments": []}
    """
    segments = points.get_correlated_segments(point_id)
    response = jsonify({'segments': segments})
    response.headers.add('Access-Control-Allow-Origin', FRONTEND_URL)
    return response


@app.route('/new_route', methods=["POST"])
@auto.doc()
def insert_route():
    """
    Insert a new route to the database, as a json string representing the Route object
    :return: response 200 if success
    """
    route = json.loads(request.data)

    route_id = routes.insert_new_route(route)

    response = jsonify({"status": 200, "route_id": route_id})
    response.headers.add('Access-Control-Allow-Origin', FRONTEND_URL)
    return response


@app.route('/update_route/<route_id>', methods=["POST"])
@auto.doc()
def update_route(route_id):
    """
    Update an existing route, as a json string representing the Route object
    :param route_id: id of the route to update
    :return: response 200 if success
    """
    route = json.loads(request.data)

    routes.update_route(route_id, route)

    response = jsonify({"status": 200})
    response.headers.add('Access-Control-Allow-Origin', FRONTEND_URL)
    return response


@app.route('/delete_route/<route_id>', methods=["POST"])
@auto.doc()
def delete_route(route_id):
    """
    Delete an existing route
    :param route_id: id of the route to delete
    :return: response 200 if success
    """
    routes.delete_route(route_id)

    response = jsonify({"status": 200})
    response.headers.add('Access-Control-Allow-Origin', FRONTEND_URL)
    return response


@app.route('/routes/<tourist_id>')
@auto.doc()
def route_list(tourist_id):
    """
    Obtain all routes that belong to the specific tourist
    :param tourist_id: id of the tourist
    :return: A json string of route names and ids in format [(route_name, route_id)]
    """
    all_routes = routes.get_route_names(tourist_id)
    response = jsonify({"routes": all_routes})
    response.headers.add('Access-Control-Allow-Origin', FRONTEND_URL)
    return response


@app.route('/route/full/<route_id>')
@auto.doc()
def full_route(route_id):
    """
    Obtain a route instance
    :param route_id: id of the route
    :return: A json string representing a route object
    """
    route = routes.get_full_route(route_id)
    response = jsonify(route)
    response.headers.add('Access-Control-Allow-Origin', FRONTEND_URL)
    return response


@app.route('/route/<tourist_id>/<route_id>/documentation', methods=['POST'])
@auto.doc()
def documentation_upload(tourist_id, route_id):
    """
    Upload a documentation file corresponding to a specific route and tourist
    :param tourist_id: id of the tourist
    :param route_id: id of the route
    :return: redirect to the documentation page if success
    """
    if 'file' not in request.files:
        return {"error": "no file"}, 400

    file = request.files['file']

    if not file.filename:
        return {"error": "no filename"}, 400
    else:
        filename = secure_filename(file.filename)
        filename, full_path = manager.get_storage(filename, tourist_id, route_id)
        file.save(os.path.join(full_path))

        routes.add_documentation(route_id, filename)

        return redirect(f"{FRONTEND_URL}/route/{tourist_id}/{route_id}/documentation")


@app.route('/documentation/<tourist_id>/<route_id>/<image>')
@auto.doc()
def documentation(tourist_id, route_id, image):
    """
    Obtain a specific documentation image
    :param tourist_id: id of the tourist
    :param route_id: id of the route
    :param image: documentation file name
    :return: A documentation file
    """
    image_path = manager.get_documentation(tourist_id, route_id, image)
    return send_file(image_path)


@app.route('/documentation/<route_id>')
@auto.doc()
def get_all_documentation(route_id):
    """
    Obtain all documentation image names corresponding to the specified route
    :param route_id: id of the route
    :return: A json string of documentation files in format {"documentation": []}
    """
    return jsonify({"documentation": routes.get_all_documentation(route_id)})


@app.route('/docs')
def docs():
    return auto.html()


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
