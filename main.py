import os
import platform
from flask import Flask

app = Flask(__name__)

# Root
@app.route("/", methods=['GET'])
def helloWorld():
    return "welcome to NYC Virtul library"


if __name__ == "__main__":
    if platform.system() == 'Linux':
        # Linux HOST
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, threaded=True)
    else:
        # Windows HOST
        app.run(port=5000, debug=True, host='127.0.0.1')
    