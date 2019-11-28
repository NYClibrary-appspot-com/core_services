# from google.cloud import storage
# from pymongo import MongoClient

# rawPath = "serviceAccount.json"
# client = storage.Client.from_service_account_json(rawPath)
# bucket_name = 'librarybucket1'
# bucket = client.get_bucket(bucket_name)

# # for bucket in client.list_buckets():
# #     print (bucket)
# #     # bucket_list = ["librarybucket1", "replica1", "replica2"]




# mongo_client = MongoClient(
#     "mongodb+srv://tweet:nKzHTG4VmIAHlKpz@twiter-pyyhe.mongodb.net/test?retryWrites=true&w=majority")
# db = mongo_client.TWITER
# db_tracker = db.db_checker

# print(db_tracker.find_one({"dbname":"replica1"}))
mongo_messagage = "both google tcp and mongoclient run on same port '2701', need to resolve the conflict"