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
    tab = []
    mycol = db["airports"]
    for x in mycol.find():
        tab.append(x)
    return render_template('index.html',tab = tab)

if __name__ == "__main__":
    app.run()