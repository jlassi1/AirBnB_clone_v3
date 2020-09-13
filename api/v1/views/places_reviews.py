#!/usr/bin/python3
"""review place objects that handles all default RestFul API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.review import Review


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False)
@app_views.route(
    '/reviews/<review_id>',
    methods=['GET'],
    strict_slashes=False)
def place_reviews(place_id=None, review_id=None):
    """get review place """
    if review_id:
        if storage.get(Review, review_id):
            return jsonify(storage.get(Review, review_id).to_dict())
        else:
            abort(404)
    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        list_reviews = []
        for review in place.reviews:
            list_reviews.append(review.to_dict())
        return jsonify(list_reviews)
    else:
        abort(404)


@app_views.route(
    '/reviews/<review_id>', methods=['DELETE'],
    strict_slashes=False)
def del_review(review_id=None):
    """ delete review"""
    if storage.get(Review, review_id):
        storage.delete(storage.get(Review, review_id))
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route(
    '/places/<place_id>/reviews', methods=['POST'],
    strict_slashes=False)
def post_review(place_id=None):
    """ post review """
    place = storage.get(place, place_id)
    if place:
        review = request.get_json()
        if not review:
            abort(400, "Not a JSON")
        if "user_id" not in review:
            abort(400, "Missing user_id")
        if not storage.get("User", review["user_id"]):
            abort(404)
        if "text" not in review:
            abort(400, "Missing text")
        else:
            review['place_id'] = place.id
            new_review = review(**review)
            storage.new(new_review)
            storage.save()
            return jsonify(new_review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id=None):
    """ put review """
    review = storage.get(Review, review_id)
    if review:
        updated = request.get_json()
        if not updated:
            abort(400, "Not a JSON")
        for k, v in updated.items():
            if k not in ['id', 'created_at', 'updated_at',
                         'user_id', 'place_id']:
                setattr(review, k, v)
        storage.save()
        return jsonify(review.to_dict()), 200
    abort(404)
