from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask import Flask
from flask import jsonify
from flask import request



client = MongoClient("mongodb://192.168.0.39:27017")
db = client.business

app = Flask(__name__)

mongo = PyMongo(app)

@app.route('/rating/<int:number>/', methods=['GET'])

def get_rating(number):

    review = db.reviews.find_one({'rating': number})
    review['_id'] = str(review['_id'])

    return jsonify({'result': [review]})


@app.route('/rating', methods=['GET'])

def get_all_ratings():

  output = []

  for resturant in db.reviews.find():

    resturant['_id'] = str(resturant['_id'])
    output.append({'_id' : resturant['_id'], 'cuisine' : resturant['cuisine'], 'name' : resturant['name'], 'rating' : resturant['rating']})

  return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
