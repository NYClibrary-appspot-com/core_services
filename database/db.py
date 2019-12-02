from google.cloud import storage
from pymongo import MongoClient

rawPath = "database\\serviceAccount.json"
primary_bucket, replica_one, replica_two = 'librarybucket1', 'replica1', 'replica2'
client = storage.Client.from_service_account_json(rawPath)
# for bucket in client.list_buckets():
#     print (bucket)


mongo_client = MongoClient("mongodb+srv://tushar:Krishcu12%40@cluster0-d2vx4.mongodb.net/admin?retryWrites=true&w=majority")
database = mongo_client.BlockChain
record = database.users.find({"email":"testuser1"})
if record is not None:
    print("MongoDB database is Connected")
