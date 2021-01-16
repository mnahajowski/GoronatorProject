from flask import Flask

from endpoints.points import points

app = Flask(__name__)


@app.route("/")
def index():
    data = points.get_data_for_browser()
    return {"data": data}


if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
