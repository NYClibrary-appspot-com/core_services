import os
import json
import platform
from flask_cors import CORS
from flask import Flask, request
from google.cloud import storage


app = Flask(__name__)
CORS(app)
rawPath = "serviceAccount.json"
client = storage.Client.from_service_account_json(rawPath)
bucket_name = 'librarybucket1'
bucket = client.get_bucket(bucket_name)
book_list = client.list_blobs(bucket_name)


# Root
@app.route("/", methods=['GET'])
def helloWorld():
    return json.dumps({"Sucess": "Welcome to our library!"})


@app.route("/book_list", methods=['GET'])
def list_of_books():
    """
    :param: None
    :return: list of all available books
    """
    book_list = client.list_blobs(bucket_name)
    list = []
    try:
        for value in book_list:
            book = value.name
            list.append(book)
            return json.dumps(list)
    except Exception as e:
        print(e)
        return json.dumps({'error': "No value found"})


@app.route("/search", methods=['GET'])
def search():
    # http://127.0.0.1:5000/search?book_name=requirements.txt

    book_name = request.args.get('book_name')
    status = search_a_book(book_name)
    return status


# view without downloading the file
def search_a_book(book_name):
    blob = bucket.get_blob(book_name)
    if blob is None:
        return json.dumps({'error': "file not found"})
    else:
        return json.dumps({'success': True, 'book_name': '{}'.format(blob.name)})


@app.route('/add', methods=['PUT'])
def add_books():
    """
    http://127.0.0.1/5000/add
    body = {}
    param: book_name
    :return: 'success' or 'error'
    """
    files = request.files['file']
    file = files.__dict__['filename']
    upload_book(file)
    status = search_a_book(file)
    return status


def upload_book(file_name):
    """Downloads a blob from the bucket."""
    blob = bucket.blob(file_name)
    with open(file_name, 'rb') as my_file:
        blob.upload_from_file(my_file)


if __name__ == "__main__":
    if platform.system() == 'Linux':
        # Linux HOST
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, threaded=True)
    else:
        # Windows HOST
        app.run(port=5000, debug=True, host='127.0.0.1')
