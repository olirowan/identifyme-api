from pymongo import MongoClient
from random import randint
import hashlib


client = MongoClient("mongodb://192.168.0.39:27017")
db=client.identifytest

# This script connects to the MongoDB service.
# The first function will post a seclection of test data to a db named business
# The second function pulls data from the db. At the moment this is just a count of the 5 star resturants.

def main():

    #insert_persons()
    #insert_locations()
    read_authorisations()
    #displaydata()


def insert_persons():

    # Information for the persons database.
    person_names = ['Oli Sorbus', 'Mike Butcher', 'Lukas Racket', 'Nicky Handle']
    person_id = 0

    for person in person_names:

        person_stored_hash = hashlib.md5(person.encode('utf-8'))
        person_id += 1

        person_entry = {
            'person_id' : person_id,
            'name' : person,
            'person_stored_hash' : person_stored_hash.hexdigest()
        }

        print(person_entry)

        db.persons.insert_one(person_entry)


def insert_locations():

    # Information regarding the cameras/doors
    locations = ['Front Door', 'Mike Room', 'Living Room', 'Back Garden', 'Oli Room', 'Lukas Room', 'Nicky Room', 'Bathroom', 'Loft']
    location_id = 0

    for location in locations:

        location_id += 1

        location_entry = {
            'location_id' : location_id,
            'location' : location
        }

        print(location_entry)

        db.locations.insert_one(location_entry)


def read_authorisations():

    for x in range(1, 10):

        location_results = db.locations.find({'location_id' : x})

        for location_result in location_results:

            print(location_result)


    for y in range(1, 5):

        person_results = db.persons.find({'person_id' : y})

        for person_result in person_results:

            print(person_result)


    auths = db.auths.find()

    for auth_result in auths:

        print(auth_result)

    # auth_entry = {
    #     'person_id' : 4,
    #     'location_id' : 9,
    #     'is_authorised' : 'no'
    # }
    # db.auths.insert_one(auth_entry)

    # {"person_id": 1, "location_id": 1, "is_authorised": "yes"}
    # {"person_id": 1, "location_id": 2, "is_authorised": "no"}
    # {"person_id": 1, "location_id": 3, "is_authorised": "yes"}
    # {"person_id": 1, "location_id": 4, "is_authorised": "yes"}
    # {"person_id": 1, "location_id": 5, "is_authorised": "yes"}
    # {"person_id": 1, "location_id": 6, "is_authorised": "no"}
    # {"person_id": 1, "location_id": 7, "is_authorised": "no"}
    # {"person_id": 1, "location_id": 8, "is_authorised": "yes"}
    # {"person_id": 1, "location_id": 9, "is_authorised": "no"}
    # {"person_id": 2, "location_id": 1, "is_authorised": "yes"}
    # {"person_id": 2, "location_id": 2, "is_authorised": "yes"}
    # {"person_id": 2, "location_id": 3, "is_authorised": "yes"}
    # {"person_id": 2, "location_id": 4, "is_authorised": "yes"}
    # {"person_id": 2, "location_id": 5, "is_authorised": "no"}
    # {"person_id": 2, "location_id": 6, "is_authorised": "no"}
    # {"person_id": 2, "location_id": 7, "is_authorised": "no"}
    # {"person_id": 2, "location_id": 8, "is_authorised": "yes"}
    # {"person_id": 2, "location_id": 9, "is_authorised": "no"}
    # {"person_id": 3, "location_id": 1, "is_authorised": "yes"}
    # {"person_id": 3, "location_id": 2, "is_authorised": "no"}
    # {"person_id": 3, "location_id": 3, "is_authorised": "yes"}
    # {"person_id": 3, "location_id": 4, "is_authorised": "yes"}
    # {"person_id": 3, "location_id": 5, "is_authorised": "no"}
    # {"person_id": 3, "location_id": 6, "is_authorised": "yes"}
    # {"person_id": 3, "location_id": 7, "is_authorised": "yes"}
    # {"person_id": 3, "location_id": 8, "is_authorised": "yes"}
    # {"person_id": 3, "location_id": 9, "is_authorised": "no"}
    # {"person_id": 4, "location_id": 1, "is_authorised": "yes"}
    # {"person_id": 4, "location_id": 2, "is_authorised": "no"}
    # {"person_id": 4, "location_id": 3, "is_authorised": "yes"}
    # {"person_id": 4, "location_id": 4, "is_authorised": "yes"}
    # {"person_id": 4, "location_id": 5, "is_authorised": "no"}
    # {"person_id": 4, "location_id": 6, "is_authorised": "yes"}
    # {"person_id": 4, "location_id": 7, "is_authorised": "yes"}
    # {"person_id": 4, "location_id": 8, "is_authorised": "yes"}
    # {"person_id": 4, "location_id": 9, "is_authorised": "no"}

#def displaydata():

    #fivestar = db.reviews.find({'rating': 5}).count()
    #print(fivestar)


main()
