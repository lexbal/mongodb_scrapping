import locale
import pymongo

from flask import Flask, render_template
from pymongo import MongoClient
from mongo_db import Mongo;

mongo = Mongo()
db    = mongo.get_database()
app   = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def index():
    nb_airport_per_continent = db.airports.aggregate([
        {"$group": {"_id": "$continent", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ])

    airports_by_score = db.airports.aggregate([
        {"$group": {
            "_id": "$continent", 
            "name" : {"$first" : "$name"}, 
            "country" : {"$first" : "$country"}, 
            "maxScore": { "$max": "$score" }
        }},
        {"$sort": {"maxScore": -1}}
    ])

    return render_template('index.html',
                            nb_airport_per_continent=nb_airport_per_continent,
                            airports_by_score=airports_by_score)

if __name__ == "__main__":
    app.run()