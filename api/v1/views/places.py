#!/usr/bin/python3
"""City objects that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False)
@app_views.route(
    '/places/<place_id>',
    methods=['GET'],
    strict_slashes=False)
def cities_places(city_id=None, place_id=None):
    """place objects that handles all default RestFul API actions"""
    if place_id:
        if storage.get(Place, place_id):
            return jsonify(storage.get(Place, place_id).to_dict())
        else:
            abort(404)
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        list_places = []
        for place in city.places:
            list_places.append(place.to_dict())
        return jsonify(list_places)
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>', methods=['DELETE'],
    strict_slashes=False)
def del_place(place_id=None):
    """ delete place"""
    if storage.get(Place, place_id):
        storage.delete(storage.get(Place, place_id))
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'],
    strict_slashes=False)
def post_place(city_id=None):
    """ post place """
    from models.place import Place
    city = storage.get("City", city_id)
    if city:
        content = request.get_json()
        if not content:
            abort(400, "Not a JSON")
        if 'user_id' not in content:
            abort(400, "Missing user_id")
        user = storage.get("User", content['user_id'])
        if not user:
            abort(404)
        if 'name' not in content:
            abort(400, "Missing name")
        content['city_id'] = city.id
        place = Place(**content)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """ put place """
    place = storage.get(Place, place_id)
    if place:
        updated = request.get_json()
        if not updated:
            abort(400, "Not a JSON")
        for k, v in updated.items():
            if k not in ['id', 'created_at', 'updated_at',
                         'user_id', 'city_id']:
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200
    abort(404)
