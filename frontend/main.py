import os

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename


app = Flask(__name__)
DEBUG = True
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'images', 'storage')

app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def index():
    myList = ['Morskie Oko - Rysy', 'Adam', 'Michał']
    return render_template('index.html', data=myList)


@app.route("/SegmentView")
def segmentView():
    #data = requests.get('http://localhost:5000/GetPoints')
    #print(data.content)
    request.urlopen()
    #request.
    myList = [['Morskie Oko - Rysy', 2, 2.3, 1200], ['Maniak - Rysy', 2, 2.3, 1200]]
    return render_template('segmentView.html', data=myList)

@app.route("/routes/<route_id>/documentation/", methods=['GET', 'POST'])
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
        images = ['background.jpg'] * 5  # get images
        routes = [("Super trasa 1", 1)] * 6  # get routes + ids
        return render_template('documentation.html', routes=routes, route_id=route_id, images=images)


if __name__ == '__main__':
    app.run(host='localhost', port=12345)
