import json
from services.db import client
from cachetools import cached, TTLCache
from services.db import replica_one, replica_two, primary_bucket


# cached for 20 seconds
cache = TTLCache(maxsize=10000, ttl=20)


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
    source_blob = primary_bucket.blob(new_blob_name)
    primary_bucket.copy_blob(source_blob, replica_one, new_blob_name)
    primary_bucket.copy_blob(source_blob, replica_two, new_blob_name)


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
