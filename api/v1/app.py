#!/usr/bin/python3
"""app module """
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import make_response
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={'/*': {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ handle errors"""
    return make_response({'error': 'Not found'}, 404)


if __name__ == "__main__":
    """ main function"""
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=getenv('HBNB_API_PORT', default='5000'),
            threaded=True)
