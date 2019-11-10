from flask import Flask


app = Flask(__name__)


@app.route("/")
def home_page():
    return "Testing commits? Still Running ? what about now?"


if __name__ == "__main__":
    app.run()
