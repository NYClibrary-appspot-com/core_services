import platform
from pymongo import MongoClient
from google.cloud import storage

rawPath = None
if platform.system() == 'Linux':
    rawPath = "services/serviceAccount.json"
else:
    rawPath = "services\\serviceAccount.json"
client = storage.Client.from_service_account_json(rawPath)
# for bucket in client.list_buckets():
#     print(bucket)

primary_bucket = client.get_bucket('librarybucket2')
replica_one = client.get_bucket('replica11')
replica_two = client.get_bucket('replica22')

Mongo_client = MongoClient("mongodb://capstone:mongopassword@cluster0-shard-00-00-we2hu.mongodb.net:27017,cluster0-shard-00-01-we2hu.mongodb.net:27017,cluster0-shard-00-02-we2hu.mongodb.net:27017/client_example?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
loggingdb = Mongo_client.logging.exceptions
# record = loggingdb.find_one({"log": ""})
# print(record)
