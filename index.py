import locale
import pymongo

from flask import Flask, render_template, request
from pymongo import MongoClient
from mongo_db import Mongo;

mongo = Mongo()
db    = mongo.get_database()
app   = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def index():
    tab = []
    mycol = db["airports"]

    for x in mycol.find():
        tab.append(x)
    
    return render_template('index.html', tab=tab)

@app.route('/best')
def best():
    airports_continent_by_score = db.airports.aggregate([
        {"$group": {
            "_id": "$continent", 
            "name" : {"$first" : "$name"}, 
            "country" : {"$first" : "$country"}, 
            "maxScore": { "$max": "$score" }
        }},
        {"$sort": {"maxScore": -1}}
    ])

    airports_subregion_by_score = db.airports.aggregate([
        {"$group": {
            "_id": "$subregion", 
            "name" : {"$first" : "$name"}, 
            "country" : {"$first" : "$country"}, 
            "maxScore": { "$max": "$score" }
        }},
        {"$sort": {"maxScore": -1, "_id": 1}}
    ])

    nb_airport_per_continent = db.airports.aggregate([
        {"$group": {"_id": "$continent", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ])

    return render_template('best/index.html',
                            nb_airport_per_continent=nb_airport_per_continent,
                            airports_continent_by_score=airports_continent_by_score,
                            airports_subregion_by_score=airports_subregion_by_score)

@app.route('/countries')
def countries():
    countries = db.airports.aggregate([
        {"$group": {"_id": "$country"}},
        {"$sort": {"_id": 1}}
    ])
    return render_template('detail/aeroport_by_continent.html', countries=countries)

@app.route('/filter/country', methods=['POST'])
def filter_country():
    country  = request.form['country']
    country  = country.replace("_", " ").title()

    airports = db.airports.aggregate([
        {"$match": {"country": country}},
        {"$sort": {"country": 1}}
    ])

    restau = db.airports.aggregate([
        {"$match": {"country": country}},
        {"$sort": {"notation.restaurants_shops": 1}}
    ])

    return render_template('detail/global_data.html', airports=airports, restau=restau)

if __name__ == "__main__":
    app.run()