import os
import sys
import json
import logging
import platform
from flask_cors import CORS
from flask import Flask, request, Response
from database.client import (client, bucket, db_tracker)


app = Flask(__name__)
CORS(app)
primary = "librarybucket1"
replica_one = "replica1"
replica_two = "replica2"


# Root https://pyback.appspot.com/
@app.route("/", methods=['GET'])
def helloWorld():
    """
    http://127.0.0.1:5000
    """
    print(db_tracker.find_one({"dbname":"replica1"}))
    return json.dumps({'success': 'welcome to nyc library server'})


@app.route("/book_list", methods=['GET'])
def list_of_books():
    """
    http://127.0.0.1:5000/book_list
    :param: None
    :return: list of all available books
    """
    # try:
    book_list = bucket.list_blobs(primary)
    print(dir(book_list))
    # list = []
    for blob in book_list:
        print(blob.name)
        # book = value.name
        # list.append(book)
    # print(list)
    return "hi"
    # except Exception as e:
    #     return json.dumps({"error": "exception found"})


@app.route("/search", methods=['GET'])
def search():
    # http://127.0.0.1:5000/search?book_name=requirements.txt
    # http://127.0.0.1:5000/search?book_name=t # prefix search
    book_name = request.args.get('book_name')
    try:
        status = search_a_book(book_name)
        return status
    except Exception as e:
        return json.dumps({"error": "exception found"})


# view without downloading the file
def search_a_book(book_name):  # search by actual file name
    blob = bucket.get_blob(book_name)

    if blob is None:  # search by prefix
        pre_list = bucket.list_blobs(prefix=book_name)

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


@app.route('/add', methods=['POST'])
def add_books():
    """
    http://127.0.0.1/5000/add
    body = {}
    param: book_name
    :return: 'success' or 'error'
    """
    try:
        file = request.files['fi']
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)

        status = search_a_book(file.filename)
        if 'success' in status:
            return json.dumps({"success": "File uploaded successfully!"})
        else:
            return json.dumps({"error": "File was not uploaded"})
    except Exception as e:
        json.dumps({"error": "exception found"})


@app.route("/download_book", methods=['GET'])
def download_a_book():
    """
    Downloads a blob from the bucket.
    http://127.0.0.1:5000/download_book?book_name=FALL2019.PNG
    """
    try:
        book_name = request.args.get('book_name')
        record = search_a_book(book_name)
        if 'success' in record:
            blob = bucket.blob(book_name)
            size = sys.getsizeof(blob.download_as_string())
            response = Response(blob.download_as_string())
            response.headers.add('Content-Range'.format('bytes'), size)
            return response
        else:
            return json.dumps({'error': 'file not found'})
    except Exception as e:
        json.dumps({"error": "exception found"})


if __name__ == "__main__":
    if platform.system() == 'Linux':
        # Linux HOST
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", debug=True, port=port, threaded=True)
    else:
        # Windows HOST
        app.run(port=5000, debug=True, host='127.0.0.1', threaded=True)
