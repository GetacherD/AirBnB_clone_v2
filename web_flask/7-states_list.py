#!/usr/bin/python3
"""
Flask App
"""
from flask import Flask
from flask import render_template
from models import storage


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def get_state():
    """ get all states_list """
    state = sorted(list(storage.all('State').values()), key=lambda x: x.name)
    return render_template("7-states_list.html", state=state)


@app.teardown_appcontext
def teardown(exc=None):
    """ close connection"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
