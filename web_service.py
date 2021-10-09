from flask import Flask, jsonify, abort, request
from flask_restful import Api, abort
import redis, json

app = Flask(__name__)
api = Api(app)

people_counter = {
    'enter': 0,
    'exit': 0,
    'total': 0
}

people_status = {
    'name': '',
    'isInside': False
}

client = redis.Redis(host='redis', port=6379, db=0)

@app.route("/eyebeacon/dashboard/people_counter", methods=['POST'])
def post():
    if len(people_counter) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'enter' in request.json and type(request.json['enter']) is not int:
        abort(400)
    if 'exit' in request.json and type(request.json['exit']) is not int:
        abort(400)
    if 'total' in request.json and type(request.json['total']) is not int:
        abort(400)
    people_counter['enter'] = request.json.get(
        'enter', people_counter['enter'])
    people_counter['exit'] = request.json.get(
        'exit', people_counter['exit'])
    people_counter['total'] = request.json.get(
        'total', people_counter['total'])
    json_1 = json.dumps(people_counter)
    client.publish('http_counter', json_1)
    return jsonify({'people_counter': people_counter})

@app.route("/eyebeacon/dashboard/people_status", methods=['GET'])
def get():
    if len(people_status) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not str:
        abort(400)
    if 'isInside' in request.json and type(request.json['isInside']) is not bool:
        abort(400)
    people_status['name'] = request.json.get(
        'name', people_status['name'])
    people_status['isInside'] = request.json.get(
        'isInside', people_status['isInside'])
    json_2 = json.dumps(people_status)
    client.publish('http_status', json_2)
    return jsonify({'people_status': people_status})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)