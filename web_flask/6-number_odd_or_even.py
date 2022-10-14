#!/usr/bin/python3
"""
Flask App
"""
from flask import Flask
from flask import render_template
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


@app.route("/number_template/<int:n>", strict_slashes=False)
def render_temp(n):
    """ render template example"""
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def chek_odd_even(n):
    """ check for even and odd"""
    status = "odd"
    if n % 2 == 0:
        status = "even"
    return render_template("6-number_odd_or_even.html", n=n, e=status)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
