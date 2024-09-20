"""
RESTFul API actions for products
"""
from models import storage
from models.product import Product
from models.order import Order
from models.shop_list import Shop_list
from models.category import Category
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from


# Make retrievals storage-agnostic
@app_views.route("/orders/<order_id>/products", strict_slashes=False)
@swag_from("api_docs/products/get_order_products.yaml")
def get_order_products(order_id):
    """ Retrieve products of a selected order instance """
    order = storage.get(Order, order_id)

    if not order:
        abort(404)

    products = [linklist.product.to_dict() for linklist in order.products]

    return jsonify(products)


@app_views.route("/categories/<category_id>/products", strict_slashes=False)
@swag_from("api_docs/products/get_category_products.yaml")
def get_category_products(category_id):
    """ Retrieve products of a selected category instance """
    category = storage.get(Category, category_id)

    if not category:
        abort(404)

    products = [product.to_dict() for product in category.products]

    return jsonify(products)


@app_views.route("/shop_lists/<shop_list_id>/products", strict_slashes=False)
@swag_from("api_docs/products/get_list_products.yaml")
def get_list_products(shop_list_id):
    """ Retrieve products of a selected shop_list instance """
    shop_list = storage.get(Shop_list, shop_list_id)

    if not shop_list:
        abort(404)

    products = [
            linklist.product.to_dict()
            for linklist in shop_list.products
            ]

    return jsonify(products)


@app_views.route("/shop_lists/<shop_list_id>/products/<product_id>",
                 methods=["DELETE"], strict_slashes=False)
@swag_from("api_docs/products/delete_list_product.yaml")
def delete_list_product(shop_list_id, product_id):
    """ Deletes a shop_list product link instance """
    shop_list = storage.get(Shop_list, shop_list_id)

    if not shop_list:
        return jsonify({"error": "Invalid shop_list_id"}), 400

    if not product_id or not storage.get(Product, product_id):
        return jsonify({"error": "Invalid product_id"}), 400

    if shop_list.remove_product(product_id):
        return jsonify({}), 204
    else:
        return jsonify({"error": "product_id is not linked to list"}), 400


@app_views.route("/shop_lists/<shop_list_id>/products/<product_id>",
                 methods=["POST"], strict_slashes=False)
@swag_from("api_docs/products/add_list_product.yaml")
def add_product(shop_list_id, product_id):
    """ Adds a product or updates its quantity to a product """
    shop_list = storage.get(Shop_list, shop_list_id)

    if not shop_list:
        return jsonify({"error": "Invalid shop_list id"}), 400

    if not product_id or not storage.get(Product, product_id):
        return jsonify({"error": "Invalid product id"}), 400

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    qty = data.get("quantity", 1)

    if qty < 1:
        return jsonify({"error": "Invalid quantity"}), 400

    shop_list.set_product_qty(product_id, qty)

    return jsonify({}), 204
