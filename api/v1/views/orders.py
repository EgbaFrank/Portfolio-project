"""
RESTFul API actions for orders
"""
from models import storage
from models.order import Order
from models.shop import Shop
from models.user import User
from models.shop_list import Shop_list
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/shops/<shop_id>/orders", strict_slashes=False)
def get_shop_orders(shop_id):
    """ Retrieve orders of a selected shop instance """
    shop = storage.get(Shop, shop_id)

    if not shop:
        abort(404)

    orders = [order.to_dict() for order in shop.orders]

    return jsonify(orders)

@app_views.route("/users/<user_id>/orders", strict_slashes=False)
def get_user_orders(user_id):
    """ Retrieve orders of a selected user instance """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    orders = [order.to_dict() for order in user.orders]

    return jsonify(orders)

@app_views.route("/shop_lists/<shop_list_id>/orders", strict_slashes=False)
def get_list_orders(shop_list_id):
    """ Retrieve orders of a selected shop_list instance """
    shop_list = storage.get(Shop_list, shop_list_id)

    if not shop_list:
        abort(404)

    orders = [order.to_dict() for order in shop_list.orders]

    return jsonify(orders)

@app_views.route("/orders/<order_id>", strict_slashes=False)
def get_order(order_id):
    """ Retrieves an order instance """
    order = storage.get(Order, order_id)
    if not order:
        abort(404)

    return jsonify(order.to_dict())

@app_views.route("/orders/<order_id>", methods=["DELETE"],
        strict_slashes=False)
def delete_order(order_id):
    """ Deletes a order instance """
    order = storage.get(Order, order_id)

    if not order:
        abort(404)

    storage.delete(order)
    storage.save()

    return jsonify({}), 204

@app_views.route("/shop_lists/<shop_list_id>/orders", methods=["POST"],
        strict_slashes=False)
def create_order(shop_list_id):
    """ Creates a order instance """
    shop_list = storage.get(Shop_list, shop_list_id)

    if not shop_list:
        abort(404)

    orders = shop_list.make_order()

    order_list = [order.to_dict() for order in orders]

    return jsonify(order_list), 201

@app_views.route("/orders/<order_id>", methods=["PUT"],
        strict_slashes=False)
def update_order(order_id):
    """ Updates a order instance """
    order = storage.get(Order, order_id)

    if not order:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = [
            'id',
            'shop_list_id',
            'shop_id',
            'user_id',
            'created_at',
            'updated_at'
            ]

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(order, key, value)

    storage.save()

    return jsonify(order.to_dict())
