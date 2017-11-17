from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask import Flask
from flask import jsonify
from flask import request



client = MongoClient("mongodb://192.168.0.39:27017")
db = client.business

app = Flask(__name__)

mongo = PyMongo(app)


@app.route('/one/', methods=['GET'])

def get_one_star():

    review = db.reviews.find_one({'rating': 1})
    review['_id'] = str(review['_id'])

    return jsonify({'result': [review]})


@app.route('/two/', methods=['GET'])

def get_two_star():

    review = db.reviews.find_one({'rating': 2})
    review['_id'] = str(review['_id'])

    return jsonify({'result': [review]})


@app.route('/three/', methods=['GET'])

def get_three_star():

    review = db.reviews.find_one({'rating': 3})
    review['_id'] = str(review['_id'])

    return jsonify({'result': [review]})


@app.route('/four/', methods=['GET'])

def get_four_star():

    review = db.reviews.find_one({'rating': 4})
    review['_id'] = str(review['_id'])

    return jsonify({'result': [review]})


@app.route('/five/', methods=['GET'])

def get_five_star():

    review = db.reviews.find_one({'rating': 5})
    review['_id'] = str(review['_id'])

    return jsonify({'result': [review]})


if __name__ == '__main__':
    app.run(debug=True)
