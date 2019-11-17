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


# Root https://avian-brand-259321.appspot.com/
@app.route("/", methods=['GET'])
def helloWorld():
    return json.dumps({"success": "Welcome to our library!"})


@app.route("/book_list", methods=['GET'])
def list_of_books():
    """
    :param: None
    :return: list of all available books
    """
    try:
        book_list = client.list_blobs(bucket_name)
        list = []
        for value in book_list:
            book = value.name
            list.append(book)
        return json.dumps(list)
    except Exception as e:
        json.dumps({"error": "exception found"})


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


@app.route("/create_dir", methods=['GET'])
def create_directory():
    book_name = "requirements.txt"
    blob = bucket.blob(book_name)
    win_path = "C:\\Users\\tusha\\Downloads\\"
    blob.download_to_filename(win_path + book_name)
    return json.dumps({"path": win_path})


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
            downloads = os.path.join(os.path.join(os.path.expanduser('~')), 'Downloads')
            blob.download_to_filename(downloads + "\\" + book_name)
            return json.dumps({'book': book_name, "status": "please check the download folder"})
        else:
            return json.dumps(record)
    except Exception as e:
        json.dumps({"error": "exception found"})


if __name__ == "__main__":
    if platform.system() == 'Linux':
        # Linux HOST
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, threaded=True)
    else:
        # Windows HOST
        app.run(port=5000, debug=True, host='127.0.0.1')
