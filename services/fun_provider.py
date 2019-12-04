import json
from services.db import client
from cachetools import cached, TTLCache


# cached for 20 seconds
cache = TTLCache(maxsize=10000, ttl=20)
primary_bucket = client.get_bucket('librarybucket1')
replica_one = client.get_bucket('replica1')
replica_two = client.get_bucket('replica2')


@cached(cache)
def cached_book_list():
    book_list = client.list_blobs(replica_one)
    list = []
    for value in book_list:
        book = value.name
        list.append(book)
    return list



def copy_blob(new_blob_name):
    """Copies a blob from one bucket to another."""
    source_bucket = client.get_bucket("librarybucket1")
    source_blob = source_bucket.blob(new_blob_name)

    destination_replica_one = client.get_bucket("replica1")
    destination_replica_two = client.get_bucket("replica2")

    source_bucket.copy_blob(source_blob, destination_replica_one, new_blob_name)
    source_bucket.copy_blob(source_blob, destination_replica_two, new_blob_name)


# view without downloading the file
def search_a_book(source_replica, book_name):  # search by actual file name
    blob = source_replica.get_blob(book_name)
    if blob is None:  # search by prefix
        pre_list = source_replica.list_blobs(prefix=book_name)

        if pre_list is not None:
            list = []
            for value in pre_list:
                book = value.name
                list.append(book)
            if len(list) > 0:
                return json.dumps(list)
        return json.dumps({'error': "file not found"})
    else:
        return json.dumps({'success': True, 'book_name': '{}'.format(blob.name)})
