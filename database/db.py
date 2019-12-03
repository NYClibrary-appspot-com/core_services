from google.cloud import storage
from pymongo import MongoClient

rawPath = "database\\serviceAccount.json"
primary_bucket, replica_one, replica_two = 'librarybucket1', 'replica1', 'replica2'
client = storage.Client.from_service_account_json(rawPath)
# for bucket in client.list_buckets():
#     print (bucket)




def copy_blob(new_blob_name):
    """Copies a blob from one bucket to another."""
    source_bucket = client.get_bucket("librarybucket1")
    source_blob = source_bucket.blob(new_blob_name)

    destination_bucket_one = client.get_bucket("replica1")
    destination_bucket_two = client.get_bucket("replica2")

    source_bucket.copy_blob(source_blob, destination_bucket_one, new_blob_name)
    source_bucket.copy_blob(source_blob, destination_bucket_two, new_blob_name)




# library
# dBcNm3lvf5GJJkBr
# mongo_client = MongoClient("mongodb://library:dBcNm3lvf5GJJkBr@cluster0-shard-00-00-d2vx4.mongodb.net:27017,cluster0-shard-00-01-d2vx4.mongodb.net:27017,cluster0-shard-00-02-d2vx4.mongodb.net:27017/test?ssl=true&replicaSet=cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
# database = mongo_client.BlockChain
# # librarydata = database.librarydata
# record = database.users.find_one({"email":"testuser1"})
# if record is not None:
#     print (dir(record))
#     print("MongoDB database is Connected")

