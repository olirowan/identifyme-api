from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask import Flask
from flask import jsonify
from flask import request
import datetime

# Point the API to the MongoDB service.
client = MongoClient("mongodb://localhost:27017")

# Set the database to be used.
db = client.identifytest

app = Flask(__name__)
mongo = PyMongo(app)


# Get a location entry by name
@app.route('/request/locations/<location_name>')
def get_location_name(location_name):

    result = []
    for location in db.locations.find({'location': location_name}):
        location['_id'] = str(
            location['_id'])  # This ID needs to be converted to a string due to the JSON requirements.

        result.append({'_id': location['_id'], 'location_id': location['location_id'], 'location': location['location']})

    return jsonify({'result': [result]})


# Get a persons entry by name
@app.route('/request/employees/name/<employee_name>')
def get_employee_name(employee_name):

    result = []
    for person in db.persons.find({'name': employee_name}):
        person['_id'] = str(
            person['_id'])  # This ID needs to be converted to a string due to the JSON requirements.

        result.append({'_id': person['_id'], 'person_id': person['person_id'], 'name': person['name'], 'person_stored_hash': person['person_stored_hash']})

    return jsonify({'result': [result]})


# Get a persons entry by hash
@app.route('/request/employees/hash/<hash>')
def get_employee_hash(hash):

    result = []
    for person in db.persons.find({'person_stored_hash': hash}):
        person['_id'] = str(
            person['_id'])  # This ID needs to be converted to a string due to the JSON requirements.

        result.append({'_id': person['_id'], 'person_id': person['person_id'], 'name': person['name'], 'person_stored_hash': person['person_stored_hash']})

    return jsonify({'result': [result]})


@app.route('/request/auths/<person_id>/<location_id>')
def get_auth(person_id, location_id):

    result = []
    for auth in db.auths.find({'person_id': person_id}):
        auth['_id'] = str(
            auth['_id'])  # This ID needs to be converted to a string due to the JSON requirements.

        result.append({'_id': auth['_id'], 'person_id': auth['person_id'], 'location': auth['location_id'], 'is_authorised': auth['is_authorised']})

    return jsonify({'result': [result]})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
