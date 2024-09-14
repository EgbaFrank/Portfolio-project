"""
RESTFul API actions for shop_lists
"""
from models import storage
from models.shop_list import Shop_list
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from


# Implement add product to list
@app_views.route("/users/<user_id>/shop_lists", strict_slashes=False)
@swag_from("api_docs/shop_lists/get_user_shop_lists.yaml")
def get_shop_lists(user_id):
    """ Retrieve shop_lists of a selected user instance """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    shop_lists = [shop_list.to_dict() for shop_list in user.shop_lists]

    return jsonify(shop_lists)

@app_views.route("/shop_lists/<shop_list_id>", strict_slashes=False)
@swag_from("api_docs/shop_lists/get_shop_list.yaml")
def get_shop_list(shop_list_id):
    """ Retrieves a shop_list instance """
    shop_list = storage.get(Shop_list, shop_list_id)
    if not shop_list:
        abort(404)

    return jsonify(shop_list.to_dict())

@app_views.route("/shop_lists/<shop_list_id>", methods=["DELETE"],
        strict_slashes=False)
@swag_from("api_docs/shop_lists/delete_shop_list.yaml")
def delete_shop_list(shop_list_id):
    """ Deletes a shop_list instance """
    shop_list = storage.get(Shop_list, shop_list_id)

    if not shop_list:
        abort(404)

    storage.delete(shop_list)
    storage.save()

    return jsonify({}), 204

@app_views.route("/users/<user_id>/shop_lists", methods=["POST"],
        strict_slashes=False)
@swag_from("api_docs/shop_lists/create_shop_list.yaml")
def create_shop_list(user_id):
    """ Creates a shop_list instance """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    shop_list = user.make_shop_list()

    return jsonify(shop_list.to_dict()), 201

@app_views.route("/shop_lists/<shop_list_id>", methods=["PUT"],
        strict_slashes=False)
def update_shop_list(shop_list_id):
    """ Updates a shop_list instance """
    shop_list = storage.get(Shop_list, shop_list_id)

    if not shop_list:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ['id', 'user_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(shop_list, key, value)

    storage.save()

    return jsonify(shop_list.to_dict())
