"""
Status route
"""

from models import storage
from flask import jsonify
from api.v1.views import app_views
from models.category import Category
from models.order import Order
from models.shop import Shop
from models.shop_list import Shop_list
from models.place import Place
from models.product import Product
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns API status """
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Retrieves the number of each instance """
    classes = [Category, Order, Shop, Shop_list, Place, Product, User]
    names = ["category", "order", "shop", "shop_list", "place", "product", "user"]
    stats = {name: storage.count(cls) for cls, name in zip(classes, names)}

    return jsonify(stats)
