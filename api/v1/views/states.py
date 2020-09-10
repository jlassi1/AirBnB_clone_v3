#!/usr/bin/python3
"""States module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''retrieve all states'''
    dict = {}
    listx = []
    for obj in storage.all("State").values():
        listx.append(obj.to_dict())
    return jsonify(listx)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_state_id(state_id):
    """retrieve state with id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


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
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def PutState(state_id=None):
    """ PUT state """
    updated = storage.get("State", state_id)
    if updated is None:
        abort(404)
    state = request.get_json()
    if state is None:
        abort(400, "Not a JSON")
    for k, v in state.items():
        if k in ['id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(updated, k, v)
    storage.save()
    return jsonify(updated.to_dict()), 200
