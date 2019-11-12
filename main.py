from flask import Flask

app = Flask(__name__)

# root
@app.route("/")
def helloWorld():
    return "welcome to NYC Virtul library"


if __name__ == "__main__":
    # Windows HOST
    app.run(port=5000, debug=True, host='127.0.0.1')

    # # Linux HOST
    # app.run(port=5000, debug=True, host='0.0.0.0')