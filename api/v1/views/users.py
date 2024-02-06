#!/usr/bin/python3
""" This file contains the views implementation of
users request as blueprint"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
import json


@app_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
@app_views.route(
    "/users/<user_id>",
    methods=["GET", "DELETE", "PUT"],
    strict_slashes=False
)
def users_view(user_id=None):
    """ View function to retrieve user
    objects"""
    if request.method == "GET" and user_id is None:
        usr_objs = storage.all(User).values()
        obj_rtn = [
            obj.to_dict() for obj in usr_objs
        ]
        return jsonify(obj_rtn), 200
    if request.method == "POST" and user_id is None:
        if not request.is_json:
            #  abort(400, description="Not a JSON")
            return jsonify({"error": "Not a JSON"}), 400
        data_input = request.get_json()   # Not always dict.
        if "email" not in data_input:
            #  abort(400, "Missing email")
            return jsonify({"error": "Missing email"}), 400
        elif "password" not in data_input:
            #  abort(400, jsonify({"error": "Missing password"}))
            return jsonify({"error": "Missing password"}), 400
        else:
            neo_usr = User(**data_input)
            storage.new(neo_usr)
            storage.save()
            return jsonify(neo_usr.to_dict()), 201
    if user_id is not None:
        usr_obj = storage.get(User, user_id)
        if request.method == "GET":
            if usr_obj is None:
                abort(404)
            return jsonify(usr_obj.to_dict()), 200
        if request.method == "DELETE":
            if usr_obj is None:
                abort(404)
            storage.delete(usr_obj)
            storage.save()
            return jsonify({}), 200
        if request.method == "PUT":
            if usr_obj is None:
                abort(404)
            if not request.is_json:
                #  abort(400, description=jsonify({"error": "Not a JSON"}))
                return jsonify({"error": "Not a JSON"}), 400
            usr_data_update = request.get_json()
            usr_update = {
                key: usr_data_update[key]
                for key in usr_data_update
                if key not in [
                    "id",
                    "email",
                    "created_at",
                    "updated_at"
                ]
            }
            for k, v in usr_update.items():
                setattr(usr_obj, v)
            usr_obj.save()
            return jsonify(usr_obj.to_dict()), 200
