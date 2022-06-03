from pymongo import MongoClient

URL= "mongodb://localhost:27017"
CLIENT= MongoClient(URL)
DB= CLIENT['commerce']
COLLECTION= DB['products']

COLLECTION.insert_one({"as": 1})

print(DB)