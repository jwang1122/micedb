"""
Supported Micro-Services (CRUD):
    * /: (GET)get all mice from database
    * /mice/<id> (GET): get specific user by given id
    * /mice (POST) + user body: create a new user
    * /mice/<id> (PUT) + user body: modify existing user
    * /mice/<id> (DELETE) : remove a user by given id
"""
from flask import Flask, jsonify, redirect, request, send_file
import json
from flask_cors import CORS
from micedb import *
import uuid

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
CORS(app)
app.config.from_object(__name__)
db = MiceDB('mice.db')


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        return "you are trying sign up with email:" + email
    return """<form action="/signup" method="post">
        <input type="text" name="email" placeholder="Enter email"></input>
        <input type="submit" value="Signup"></input>
    </form>"""


@app.route('/', methods=['GET'])
def all_mice():
    response_object = {'status': 'success'}
    mice = db.getMice()
    response_object['mice'] = mice
    return jsonify(response_object)

@app.route('/createpdf', methods=['GET', 'POST'])
def get_pdf():
    return send_file('matplotlib.pdf', as_attachment=True)

@app.route('/mice', methods=['POST'])
def create_mouse():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    mouse = {'id': uuid.uuid4().hex}
    for field in MiceDB.miceFields:
        mouse[field] = post_data.get(field)
    id = db.create(mouse)
    response_object['message'] = 'mouse added!'
    return jsonify(response_object)


@app.route('/breeding', methods=['POST'])
def create_breeding():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    print(post_data)
    mouse = {
        'id': uuid.uuid4().hex,
        'dob': post_data.get('dob'),
        'cage': post_data.get('cage'),
        'mom': post_data.get('mom'),
        'dad': post_data.get('dad'),
        'born': post_data.get('born'),
        'males': post_data.get('males'),
        'females': post_data.get('females'),
        'deaths': post_data.get('deaths'),
        'notes': post_data.get('notes'),
    }
    print(mouse)
    id = db.create_breeding(mouse)
    response_object['message'] = 'mouse added!'
    return jsonify(response_object)


@app.route('/mice/<mouse_id>', methods=['GET'])
def retrieve_mouse(mouse_id):
    response_object = {'status': 'success'}
    mouse = db.getMouse(mouse_id)
    response_object['mouse'] = mouse
    return jsonify(response_object)


@app.route('/mice/<mouse_id>', methods=['DELETE'])
def delete_user(mouse_id):
    response_object = {'status': 'success'}
    id = db.delete(mouse_id)
    response_object['message'] = 'mouse deleted!'
    return jsonify(response_object)


@app.route('/mice/<mouse_id>', methods=['PUT'])
def update_user(mouse_id):
    response_object = {'status': 'success'}
    post_data = request.get_json()
    mouse = {
        'msid': post_data.get('msid'),
        'gender': post_data.get('gender'),
        'geno': post_data.get('geno'),
        'dob': post_data.get('dob'),
        'ear': post_data.get('ear'),
        'mom': post_data.get('mom'),
        'dad': post_data.get('dad'),
        'cage': post_data.get('cage'),
        'usage': post_data.get('usage'),
        'date': post_data.get('date'),
        'type': post_data.get('type'),
    }
    db.update(mouse_id, mouse)
    response_object['message'] = 'mouse updated!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
