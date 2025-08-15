import pymongo
import configparser
# Load configuration from env.ini
config = configparser.ConfigParser()
config.read('env.ini')
uri = config.get('mongodb', 'uri')

client = pymongo.MongoClient(uri)

db = client.get_database("cashback")
collection = db.get_collection("cashback")

