from pymongo import MongoClient
from random import randint


client = MongoClient("mongodb://192.168.0.39:27017")
db=client.business

# This script connects to the MongoDB service.
# The first function will post a seclection of test data to a db named business
# The second function pulls data from the db. At the moment this is just a count of the 5 star resturants.

def main():

    #insertdata()
    displaydata()


def insertdata():

    names = ['Kitchen', 'Animal', 'State', 'Tastey', 'Big', 'City', 'Fish', 'Pizza', 'Goat', 'Salty', 'Sandwich',
             'Lazy', 'Fun']

    company_type = ['LLC', 'Inc', 'Company', 'Corporation']

    company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']

    for x in xrange(1, 501):
        business = {
            'name': names[randint(0, (len(names) - 1))] + ' ' + names[randint(0, (len(names) - 1))] + ' ' +
                    company_type[randint(0, (len(company_type) - 1))],
            'rating': randint(1, 5),
            'cuisine': company_cuisine[randint(0, (len(company_cuisine) - 1))]
        }

        result = db.reviews.insert_one(business)
        print('Created {0} of 100 as {1}'.format(x, result.inserted_id))

    print('finished creating 100 business reviews')


def displaydata():

    fivestar = db.reviews.find({'rating': 5}).count()
    print(fivestar)


main()
