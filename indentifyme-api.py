from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask import Flask
from flask import jsonify
from flask import request
import datetime

# Point the API to the MongoDB service.
client = MongoClient("mongodb://localhost:27017")

# Set the database to be used.
db = "IdentifyTest"

# Set the collection to use.
collection = "Employees"

app = Flask(__name__)
mongo = PyMongo(app)


# API GET request to return one restaurant with the rating included in the URL.
@app.route('/employee/<int:idnumber>/', methods=['GET'])
def get_rating(idnumber):

    if 0 <= idnumber <= 5000:
        result = db.collection.find_one({'id': idnumber})
        result['_id'] = str(result['_id'])  # This ID needs to be converted to a string due to the JSON requirements.
    else:
        result = "You have not chosen a ID number."

    return jsonify({'result': [result]})


# A POST to the API that allows a user to add an entry to the DB.
@app.route('/identifier/<fresh_hash>', methods=['POST'])
def check_authentication(fresh_hash):

    result = []

    if fresh_hash == "":
        print("no")


    cuisine = request.json['cuisine']
    name = request.json['name']
    rating = request.json['rating']

    if cuisine == "":
        result.append("Please enter a style of cuisine. ")
    elif name == "":
        result.append("Please enter the restaurant name. ")
    elif rating == "":
        result.append("Please enter a rating.")
    else:

        review_id = db.reviews.insert({'cuisine': cuisine, 'name': name, 'rating': rating})

        new_review = db.reviews.find_one({'_id': review_id})
        new_review['_id'] = str(new_review['_id'])
        result = {'_id': new_review['_id'], 'cuisine': new_review['cuisine'], 'name': new_review['name'],
                  'rating': new_review['rating']}

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
