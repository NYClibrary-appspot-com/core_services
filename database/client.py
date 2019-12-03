from google.cloud import storage
from pymongo import MongoClient


rawPath = "database\\serviceAccount.json"
client = storage.Client.from_service_account_json(rawPath)
pimary_bucket, replica_one, replica_two = 'librarybucket1', 'replica1', 'replica2'

# all buckets
bucket_primary = client.get_bucket(pimary_bucket)
bucket_one = client.get_bucket(replica_one)
bucket_two = client.get_bucket(replica_two)

for bucket in client.list_buckets():
    print (bucket)
    # bucket_list = ["librarybucket1", "replica1", "replica2"]




mongo_client = MongoClient(
    "mongodb+srv://tweet:nKzHTG4VmIAHlKpz@twiter-pyyhe.mongodb.net/test?retryWrites=true&w=majority")
db = mongo_client["TWITER"]
db_tracker = db["db_checker"]
print(dir(db_tracker.find()))

# print(db_tracker.find_one({"dbname": "replica1"}))

# mongo_messagage = "both google tcp and mongoclient run on same port '27017', need to resolve the conflict"
# # gcloud compute firewall-rules create allow-mongodb --allow tcp:27017

# print(mongo_messagage)
