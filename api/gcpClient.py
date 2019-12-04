import sys
import json
import logging

from cachetools import cached, TTLCache
from services.db import client, loggingdb
from flask import Blueprint, request, Response


gcp_api = Blueprint('gcp_api', __name__)
primary_bucket = client.get_bucket('librarybucket1')
replica_one = client.get_bucket('replica1')
replica_two = client.get_bucket('replica2')
cache = TTLCache(maxsize=10000, ttl=60*3)


@gcp_api.route("/book_list", methods=['GET'])
def list_of_books():
    """
    :param: None
    :return: list of all available books
    """
    try:
        return json.dumps(cached_book_list())
    except Exception as e:
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')
        with open('myapp.log') as log:
            line = log.readline()
            if line is not None:
                loggingdb.insert_one({'log': str(line)})
        return json.dumps({"error": "exception found"})


@gcp_api.route("/search", methods=['GET'])
def search():
    # http://127.0.0.1:5000/search?book_name=requirements.txt
    # http://127.0.0.1:5000/search?book_name=t # prefix search
    book_name = request.args.get('book_name')
    try:
        status = search_a_book(book_name)
        copy_blob(book_name)
        return status
    except Exception as e:
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')
        with open('myapp.log') as log:
            line = log.readline()
            if line is not None:
                loggingdb.insert_one({'log': str(line)})
        return json.dumps({"error": "exception found , code:404"})


# view without downloading the file
def search_a_book(book_name):  # search by actual file name
    blob = replica_one.get_blob(book_name)
    if blob is None:  # search by prefix
        pre_list = replica_one.list_blobs(prefix=book_name)

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


@gcp_api.route('/add', methods=['POST'])
def add_books():
    """
    http://127.0.0.1/5000/add
    body = {}
    param: book_name
    :return: 'success' or 'error'
    """
    try:
        file = request.files['fi']
        blob = primary_bucket.blob(file.filename)
        blob.upload_from_file(file)

        status = primary_bucket.get_blob(file.filename)
        if status is not None:
            copy_blob(file.filename)
            return json.dumps({"success": "File uploaded successfully!"})
        else:
            return json.dumps({"error": "File was not uploaded"})
    except Exception as e:
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')
        with open('myapp.log') as log:
            line = log.readline()
            if line is not None:
                loggingdb.insert_one({'log': str(line)})
        return json.dumps({"error": "exception found"})


@gcp_api.route("/download_book", methods=['GET'])
def download_a_book():
    """
    Downloads a blob from the bucket.
    http://127.0.0.1:5000/download_book?book_name=FALL2019.PNG
    """
    try:
        book_name = request.args.get('book_name')
        record = search_a_book(book_name)
        if 'success' in record:
            blob = replica_one.blob(book_name)
            size = sys.getsizeof(blob.download_as_string())
            response = Response(blob.download_as_string())
            response.headers.add('Content-Range'.format('bytes'), size)
            return response
        else:
            return json.dumps({'error': 'file not found'})
    except Exception as e:
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')
        with open('myapp.log') as log:
            line = log.readline()
            if line is not None:
                loggingdb.insert_one({'log': str(line)})
        return json.dumps({"error": "exception found"})


def copy_blob(new_blob_name):
    """Copies a blob from one bucket to another."""
    source_bucket = client.get_bucket("librarybucket1")
    source_blob = source_bucket.blob(new_blob_name)

    destination_replica_one = client.get_bucket("replica1")
    destination_replica_two = client.get_bucket("replica2")

    source_bucket.copy_blob(source_blob, destination_replica_one, new_blob_name)
    source_bucket.copy_blob(source_blob, destination_replica_two, new_blob_name)


@cached(cache)
def cached_book_list():
    book_list = client.list_blobs(replica_one)
    list = []
    for value in book_list:
        book = value.name
        list.append(book)
    return list
