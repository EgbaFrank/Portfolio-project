"""
RESTFul API actions for Categories
"""
from models.category import Category
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/categories", strict_slashes=False)
@app_views.route("/categories/<category_id>", strict_slashes=False)
def get_category(category_id=None):
    """Retrieves all or a specific category"""
    if not category_id:
        categories = storage.all(Category).values()
        categories_list = [category.to_dict() for category in categories]

        return jsonify(categories_list)

    else:
        category = storage.get(Category, category_id)

        if not category:
            abort(404)

        return jsonify(category.to_dict())


@app_views.route("/categories/<category_id>", methods=["DELETE"],
        strict_slashes=False)
def delete_category(category_id):
    """ Deletes a category """
    category = storage.get(Category, category_id)

    if not category:
        abort(404)

    storage.delete(category)
    storage.save()

    return jsonify({}), 204


@app_views.route("/categories", methods=["POST"],
        strict_slashes=False)
def create_category():
    """ Creates a category instance """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_category = Category(**data)
    new_category.save()

    return jsonify(new_category.to_dict()), 201

@app_views.route("/categories/<category_id>", methods=["PUT"],
        strict_slashes=False)
def update_category(category_id):
    """ Updates a category instance """
    category = storage.get(Category, category_id)

    if not category:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(category, key, value)

    category.save()
    return jsonify(category.to_dict())

