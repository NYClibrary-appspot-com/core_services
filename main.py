import os
import json
import time
import platform

from flask import Flask
from flask_cors import CORS
from api.gcp_api import gcp_api

app = Flask(__name__)
CORS(app)
app.register_blueprint(gcp_api, url_prefix='')


# Root https://pyback.appspot.com/
@app.route("/", methods=['GET'])
def helloWorld():
    """
    http://127.0.0.1:5000
    """
    return json.dumps({'success': 'welcome to nyc library server'})


@app.route("/2", methods=['GET'])
def helloWorld2():
    """
    http://127.0.0.1:5000
    """
    print(time.ctime())
    return json.dumps({'success': 'welcome to nyc library server'})


if __name__ == "__main__":
    if platform.system() == 'Linux':
        # Linux HOST
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, threaded=True)
    else:
        # Windows HOST
        app.run(port=5000, debug=True, host='127.0.0.1')
