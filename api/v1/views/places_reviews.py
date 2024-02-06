#!/usr/bin/python3
"""This module contains the view for the place resource."""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route(
    "/places/<place_id>/reviews",
    strict_slashes=False,
    methods=["GET", "POST"]
)
def get_plc_reviews(place_id):
    """ Function to get the reviws
    of a place_id"""
    place_obj = storage.get(Place, place_id)
    if request.method == "GET":
        if place_obj is None:
            abort(404)
        return jsonify(
            [obj.to_dict() for obj in place_obj.reviews]
        )
    if request.method == "POST":
        if place_obj is None:
            abort(404)
        if not request.is_json:
            abort(400, "Not a JSON")
        json_data = request.get_json()
        if "user_id" not in json_data:
            abort(400, "Missing user_id")
        reviewer_usr_obj = storage.get(User, json_data["user_id"])
        if reviewer_usr_obj is None:
            abort(404)
        if "text" not in json_data:
            abort(400, "Missing text")
        json_data["place_id"] = place_id
        neo_review_obj = Review(**json_data)
        storage.new(neo_review_obj)
        storage.save()
        return jsonify(neo_review_obj.to_dict()), 201


@app_views.route(
    "/reviews/<review_id>",
    strict_slashes=False,
    methods=["GET", "DELETE", "PUT"]
)
def get_plc_review(review_id):
    """Function to get a particular review using
    review_id from the list of reviews"""
    review_object = storage.get(Review, review_id)
    if request.method == "GET":
        if not review_object:
            abort(404)
        return jsonify(review_object.to_dict())
    if request.method == "DELETE":
        if not review_object:
            abort(404)
        storage.delete(review_object)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        if not review_object:
            abort(404)
        if not request.is_json:
            abort(400, "Not a JSON")
        json_data = request.get_json()
        for key, value in json_data.items():
            if key not in [
                "id", "user_id", "place_id",
                "created_at", "updated_at"
            ]:
                setattr(review_object, key, value)
        review_object.save()
        #  storage.save()
        return jsonify(review_object.to_dict()), 200
