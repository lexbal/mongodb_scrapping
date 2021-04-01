import os;
import pymongo;
from pymongo import MongoClient;
from dotenv import load_dotenv;

load_dotenv()

class Mongo(object):
    
    __host     = os.getenv("MONGO_HOST")
    __database = os.getenv("MONGO_DBNAME")
    __client   = None

    def __init__(self):
        if not self.__client:
            try:
                self.__client = MongoClient(self.__host)
            except pymongo.errors.ConnectionFailure:
                print("Failed to connect to server {}".format(self.__host)) 

    def get_client(self):
        return self.__client

    def get_database(self, dbname = None):
        client = self.get_client()
        dbname = dbname if dbname is not None else self.__database

        if dbname in client.list_database_names():
            return client[dbname]
        
        return None