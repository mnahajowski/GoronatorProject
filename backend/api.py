from flask import Flask

from endpoints.points import points

app = Flask(__name__)


@app.route("/route_segments")
def index():
    all_points = points.get_points()
    all_segments = points.get_segments()
    return {"points": all_points, "segments": all_segments}


@app.route("/segment/<segment_list>")
def segments_by_id(segment_list):
    segment_list = segment_list.split(',')
    all_segments = points.get_segments_by_ids(segment_list)

    return {"segments": all_segments}


@app.route('/point/<point_list>')
def points_by_id(point_list):
    point_list = point_list.split(',')
    all_points = points.get_points_by_id(point_list)

    return {"points": all_points}


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
