#!/usr/bin/python3
"""
The app
"""

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    The teardown function
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    To handle 404 error
    :return: returns 404 json
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return (resp)


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
