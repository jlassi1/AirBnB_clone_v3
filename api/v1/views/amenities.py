#!/usr/bin/python3
"""Amenitiy module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route(
    '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenities(amenity_id=None):
    """amenity objects that handles all default RestFul API actions"""
    if amenity_id is None:
        list_amenities = []
        for amenity in storage.all(Amenity).values():
            list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)
    elif storage.get(Amenity, amenity_id):
        return jsonify(storage.get(Amenity, amenity_id).to_dict())
    else:
        abort(404)


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'],
    strict_slashes=False)
def del_amenity(amenity_id=None):
    """ delete amenity"""
    if storage.get(Amenity, amenity_id):
        storage.delete(storage.get(Amenity, amenity_id))
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ post amenity """
    amenity = request.get_json()
    if amenity is None:
        abort(400, "Not a JSON")
    elif "name" not in amenity.keys():
        abort(400, "Missing name")
    else:
        new_amenity = Amenity(**amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id=None):
    """ put amenity """
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
