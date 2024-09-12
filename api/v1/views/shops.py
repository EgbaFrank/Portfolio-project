"""
RESTFul API actions for shops
"""
from models import storage
from models.shop import Shop
from models.place import Place
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/places/<place_id>/shops", strict_slashes=False)
def get_shops(place_id):
    """ Retrieve shops of a selected place instance """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    shops = [shop.to_dict() for shop in place.shops]

    return jsonify(shops)

@app_views.route("/shops/<shop_id>", strict_slashes=False)
def get_shop(shop_id):
    """ Retrieves a shop instance """
    shop = storage.get(Shop, shop_id)
    if not shop:
        abort(404)

    return jsonify(shop.to_dict())

@app_views.route("/shops/<shop_id>", methods=["DELETE"],
        strict_slashes=False)
def delete_shop(shop_id):
    """ Deletes a shop instance """
    shop = storage.get(Shop, shop_id)

    if not shop:
        abort(404)

    storage.delete(shop)
    storage.save()

    return jsonify({}), 204

@app_views.route("/places/<place_id>/shops", methods=["POST"],
        strict_slashes=False)
def create_shop(place_id):
    """ Creates a shop instance """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    data["place_id"] = place_id

    new_shop = Shop(**data)
    new_shop.save()

    return jsonify(new_shop.to_dict()), 201

@app_views.route("/shops/<shop_id>", methods=["PUT"],
        strict_slashes=False)
def update_shop(shop_id):
    """ Updates a shop instance """
    shop = storage.get(Shop, shop_id)

    if not shop:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ['id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(shop, key, value)

    storage.save()

    return jsonify(shop.to_dict())
