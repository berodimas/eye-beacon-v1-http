from flask import Flask, jsonify, abort, request
from flask_restful import Api, abort
import redis, json, argparse

app = Flask(__name__)
api = Api(app)

counter = {
    'enter': 0,
    'exit': 0,
    'total': 0
}

status = {
    'name': '',
    'isInside': False,
    'room': ''
}

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", type=str,
                help="url for http host")
ap.add_argument("-p", "--port", type=int,
                help="port for http host")
ap.add_argument("-r", "--redis", type=str,
                help="input for redis host")
args = vars(ap.parse_args())

r = redis.Redis(host=args["redis"], port=6379, db=0)

@app.route("/eyebeacon/dashboard/counter", methods=['POST'])
def handler_counter():
    if len(counter) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'enter' in request.json and type(request.json['enter']) is not int:
        abort(400)
    if 'exit' in request.json and type(request.json['exit']) is not int:
        abort(400)
    if 'total' in request.json and type(request.json['total']) is not int:
        abort(400)
    counter['enter'] = request.json.get(
        'enter', counter['enter'])
    counter['exit'] = request.json.get(
        'exit', counter['exit'])
    counter['total'] = request.json.get(
        'total', counter['total'])
    responese = json.dumps(counter)
    r.publish('http_counter', responese)
    return jsonify({'counter': counter})

@app.route("/eyebeacon/dashboard/status/<room>", methods=['POST'])
def handler_status(room):
    if len(status) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not str:
        abort(400)
    if 'isInside' in request.json and type(request.json['isInside']) is not bool:
        abort(400)
    status['name'] = request.json.get(
        'name', status['name'])
    status['isInside'] = request.json.get(
        'isInside', status['isInside'])
    status['room'] = room
    responese = json.dumps(status)
    r.publish('http_status', responese)
    return jsonify({'status': status})

if __name__ == "__main__":
    app.run(host=args["url"], port=args["port"])
