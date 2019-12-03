import platform
from google.cloud import storage
from pymongo import MongoClient

rawPath = None
if platform.system() == 'Linux':
    rawPath = "database/serviceAccount.json"
else:
    rawPath = "database\\serviceAccount.json"
client = storage.Client.from_service_account_json(rawPath)
# for bucket in client.list_buckets():
#     print (bucket)



# library
# dBcNm3lvf5GJJkBr
# mongo_client = MongoClient("mongodb://library:dBcNm3lvf5GJJkBr@cluster0-shard-00-00-d2vx4.mongodb.net:27017,cluster0-shard-00-01-d2vx4.mongodb.net:27017,cluster0-shard-00-02-d2vx4.mongodb.net:27017/test?ssl=true&replicaSet=cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
# database = mongo_client.BlockChain
# # librarydata = database.librarydata
# record = database.users.find_one({"email":"testuser1"})
# if record is not None:
#     print (dir(record))
#     print("MongoDB database is Connected")

