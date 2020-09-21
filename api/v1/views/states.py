#!/usr/bin/python3
"""users module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import state


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states(state_id=None):
    """state objects that handles all default RestFul API actions"""
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
        abort(400, "Not a JSON")
    elif "email" not in state.keys():
        abort(400, "Missing email")
    elif "password" not in state.keys():
        abort(400, "Missing password")
    else:
        new_state = State(**state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """ put state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    update = request.get_json()
    if update is None:
        abort(400, "Not a JSON")
    for k, v in update.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(State, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
