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



if __name__ == '__main__':
    app.run(debug=True)
