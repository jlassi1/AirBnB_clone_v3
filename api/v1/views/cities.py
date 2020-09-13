#!/usr/bin/python3
"""State objects that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
@app_views.route(
    '/cities/<city_id>',
    methods=['GET'],
    strict_slashes=False)
def states_cities(state_id=None, city_id=None):
    """State objects that handles all default RestFul API actions"""
    if city_id is not None:
        if storage.get(City, city_id):
            return jsonify(storage.get(City, city_id).to_dict())
        else:
            abort(404)
    if state_id is not None:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        list_cities = []
        for cities in storage.all(City).values():
            if cities.id == state_id:
                list_cities.append(cities.to_dict())
        return jsonify(list_cities)
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>', methods=['DELETE'],
    strict_slashes=False)
def del_city(city_id=None):
    """ delete city"""
    if storage.get(City, city_id):
        storage.delete(storage.get(City, city_id))
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>/cities', methods=['POST'],
    strict_slashes=False)
def post_city(state_id):
    """ post city """
    if not storage.get(State, state_id):
        abort(404)
    city = request.get_json()
    if city is None:
        abort(400, "Not a JSON")
    elif "name" not in city.keys():
        abort(400, "Missing name")
    else:
        new_city = City(**city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    """ PUT city """
    city = request.get_json()
    if city is None:
        abort(400, "Not a JSON")
    updated = storage.get(City, city_id)
    if updated is None:
        abort(404)
    for k, v in city.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(updated, k, v)
    storage.save()
    return jsonify(updated.to_dict()), 200
