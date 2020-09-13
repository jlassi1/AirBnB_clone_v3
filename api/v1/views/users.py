#!/usr/bin/python3
"""users module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users(user_id=None):
    """user objects that handles all default RestFul API actions"""
    if user_id is None:
        list_users = []
        for user in storage.all(User).values():
            list_users.append(user.to_dict())
        return jsonify(list_users)
    elif storage.get(user, user_id):
        return jsonify(storage.get(User, user_id).to_dict())
    else:
        abort(404)


@app_views.route(
    '/users/<user_id>', methods=['DELETE'],
    strict_slashes=False)
def del_user(user_id=None):
    """ delete user"""
    if storage.get(User, user_id):
        storage.delete(storage.get(User, user_id))
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ post user """
    user = request.get_json()
    if user is None:
        abort(400, "Not a JSON")
    elif "email" not in user.keys():
        abort(400, "Missing email")
    elif "password" not in user.keys():
        abort(400, "Missing password")
    else:
        new_user = User(**user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """ put user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    update = request.get_json()
    if update is None:
        abort(400, "Not a JSON")
    for k, v in update.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
