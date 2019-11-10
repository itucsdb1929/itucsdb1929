from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home_page():
    return "Testing commits? Still Running ? what about now?"

@app.route('/<user>')
def hello_name(user):
    return render_template('base.html', name = user)


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000, debug=True)
