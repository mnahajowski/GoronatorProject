from flask import Flask, render_template
import requests
from urllib import request
app = Flask(__name__)
DEBUG = True
app.config.from_object(__name__)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
