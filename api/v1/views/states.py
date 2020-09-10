#!/usr/bin/python3
"""States module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states(state_id=None):
    """State objects that handles all default RestFul API actions"""
    if state_id is None:
        list_states = []
        for state in storage.all(State).values():
            list_states.append(state.to_dict())
        return jsonify(list_states)
    elif storage.get(State, state_id):
        return jsonify(storage.get(State, state_id).to_dict())
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'],
    strict_slashes=False)
def del_state(state_id=None):
    """ delete state"""
    if storage.get(State, state_id):
        storage.delete(storage.get(State, state_id))
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ post state """
    state = request.get_json()
    if state is None:
        abort(400, message="Not a JSON")
    elif "name" not in state.keys():
        abort(400, message="Missing name")
    else:
        new_state = State(**state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updating  a state"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
