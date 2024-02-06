#!/usr/bin/python3
""" The implementation of blueprint for index routing behaviour"""
from flask import jsonify
from api.v1.views import app_views

from models import storage


@app_views.route("/status")
def status():
    from flask import jsonify

    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    app_class_names = {
        Amenity: "amenities", City: "cities", Place: "places",
        Review: "reviews", State: "states", User: "users"

    }
    app_class_cnts = {
        Amenity: 0, City: 0, Place: 0,
        Review: 0, State: 0, User: 0
    }

    for cls in app_class_cnts.keys():
        app_class_cnts[cls] = storage.count(cls)

    return jsonify({app_class_names[k]: v for k, v in app_class_cnts.items()})
