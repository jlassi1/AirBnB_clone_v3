#!flask/bin/python
""" """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ """
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def status_count():
    """ """
    clss = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
        }
    dic = {}
    for key, val in clss.items():
        dic[val] = storage.count(key)
    return jsonify(dic)