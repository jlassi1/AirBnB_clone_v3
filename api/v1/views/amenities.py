#!/usr/bin/python3
"""Amenitiy module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def post_amenity():
    """ post amenity """
    if request.methods == "POST":
        amenity = request.get_json()
        if amenity is None:
            abort(400, "Not a JSON")
        elif "name" not in amenity.keys():
            abort(400, "Missing name")
        else:
            new_amenity = Amenity(**amenity)
            storage.save()
            return jsonify(new_amenity.to_dict()), 201
    if request.methods == "GET":
        list_amenities = []
        for amenity in storage.all(Amenity).values():
            list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET', 'DELETE', "PUT"],
    strict_slashes=False)
def amenities(amenity_id=None):
    """amenity objects that handles all default RestFul API actions"""
    if request.methods == "GET":
        if storage.get(Amenity, amenity_id):
            return jsonify(storage.get(Amenity, amenity_id).to_dict())
        else:
            abort(404)
    if request.methods == "DELETE":
        if storage.get(Amenity, amenity_id):
            storage.delete(storage.get(Amenity, amenity_id))
            storage.save()
            return jsonify({})
        else:
            abort(404)
    if request.methods == "PUT":
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        update = request.get_json()
        if update is None:
            abort(400, "Not a JSON")
        for k, v in update.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, k, v)
        storage.save()
        return jsonify(amenity.to_dict()), 200
