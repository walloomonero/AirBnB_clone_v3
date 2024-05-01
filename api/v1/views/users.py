#!/usr/bin/python3
"""
The route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    To retrieve all User objects
    :return: The json of all users
    """
    user_list = []
    user_obj = storage.all("User")
    for obj in user_obj.values():
        user_list.append(obj.to_json())

    return jsonify(user_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    To create user route
    :return: The newly created user obj
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    resp = jsonify(new_user.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    To get a specific User object by ID
    :parameter user_id: user object id
    :return: The user obj with the specified id or error
    """

    fetched_obj = storage.get("User", str(user_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    To update specific User object by ID
    :parameter user_id: user object ID
    :return: The user object and 200 on success, or 400 or 404 on failure
    """
    user_json = request.get_json(silent=True)

    if user_json is None:
        abort(400, 'Not a JSON')

    fetched_obj = storage.get("User", str(user_id))

    if fetched_obj is None:
        abort(404)

    for key, val in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetched_obj, key, val)

    fetched_obj.save()

    return jsonify(fetched_obj.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    To delete User by id
    :parameter user_id: user object id
    :return: The empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get("User", str(user_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
