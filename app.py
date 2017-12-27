from gevent import monkey; monkey.patch_all()

import json
import os

from bottle import abort, Bottle, run, static_file, response, request


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

app = Bottle()
@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.get("/")
def index():
    return static_file("index.html", BASE_DIR)


@app.get("/assets/<fname:path>")
def assets(fname):
    return static_file(fname, os.path.join(BASE_DIR, "assets"))


@app.route("/api/v1/albums/", method=['OPTIONS', 'GET'])
def albums():
    if request.method == 'OPTIONS':
        return {}
    fname = "data/albums/index.json"
    if not os.path.exists(fname):
        abort(404)
    with open(fname) as fd:
        return json.load(fd)



@app.route("/api/v1/albums/<album_id:int>/", method=['OPTIONS', 'GET'])
def album(album_id):
    if request.method == 'OPTIONS':
        return {}
    fname = "data/albums/{}.json".format(album_id)
    if not os.path.exists(fname):
        abort(404)
    with open(fname) as fd:
        return json.load(fd)


if __name__ == "__main__":
    run(app, host="localhost", port=8080, server='gevent')
