from flask import Flask

from endpoints.points import points

app = Flask(__name__)


@app.route("/")
def index():
    all_points = points.get_points()
    all_segments = points.get_segments()
    return {"points": all_points, "segments": all_segments}


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
