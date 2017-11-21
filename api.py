from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask import Flask
from flask import jsonify
from flask import request

client = MongoClient("mongodb://192.168.0.39:27017")
db = client.business

app = Flask(__name__)
mongo = PyMongo(app)


# API GET request to return one restaurant with the rating included in the URL.
@app.route('/rating/<int:number>/', methods=['GET'])
def get_rating(number):

    if 0 <= number <= 5:
        result = db.reviews.find_one({'rating': number})
        result['_id'] = str(result['_id'])  # This ID needs to be converted to a string due to the JSON requirements.
    else:
        result = "You have not chosen a valid rating value."

    return jsonify({'result': [result]})


# API GET request to return all restaurants with the cuisine included in the URL.
@app.route('/cuisine/<cuisine>/', methods=['GET'])
def get_cuisine(cuisine):

    result = []
    for resturant in db.reviews.find({'cuisine': cuisine}):
        resturant['_id'] = str(
            resturant['_id'])  # This ID needs to be converted to a string due to the JSON requirements.

        result.append({'_id': resturant['_id'], 'cuisine': resturant['cuisine'], 'name': resturant['name'],
                       'rating': resturant['rating']})

    return jsonify({'result': [result]})


# Another GET request to return every entry in the table.
@app.route('/rating', methods=['GET'])
def get_all_ratings():

    result = []
    for resturant in db.reviews.find():
        resturant['_id'] = str(resturant['_id'])
        result.append({'_id': resturant['_id'], 'cuisine': resturant['cuisine'], 'name': resturant['name'],
                       'rating': resturant['rating']})

    return jsonify({'result': result})


# A POST to the API that allows a user to add an entry to the DB.
@app.route('/rating', methods=['POST'])
def add_rating():

    result = []

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
