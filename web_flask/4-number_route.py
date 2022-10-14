#!/usr/bin/python3
"""
Flask App
"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """ Index Page """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_home():
    """ Display hbnb home"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def get_variable(text):
    """ accept variable in url """
    value = text.replace("_", " ")
    return "C {}".format(value)


@app.route("/python/", defaults={"text": "is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def default_variable(text):
    """ accept variable in url with some default"""
    value = text.replace("_", " ")
    return "Python {}".format(value)


@app.route("/number/<int:n>", strict_slashes=False)
def get_number(n):
    """ get number from url"""
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
