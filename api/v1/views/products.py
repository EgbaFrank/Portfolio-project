"""
RESTFul API actions for products
"""
from models import storage
from models.product import Product
from models.shop import Shop
from models.category import Category
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from


@app_views.route("/shops/<shop_id>/products", strict_slashes=False)
@swag_from("api_docs/products/get_shop_products.yaml")
def get_shop_products(shop_id):
    """ Retrieve products of a selected shop instance """
    shop = storage.get(Shop, shop_id)

    if not shop:
        abort(404)

    products = [product.to_dict() for product in shop.products]

    return jsonify(products)


@app_views.route("/products/<product_id>", strict_slashes=False)
@swag_from("api_docs/products/get_product.yaml")
def get_product(product_id):
    """ Retrieves a product instance """
    product = storage.get(Product, product_id)
    if not product:
        abort(404)

    return jsonify(product.to_dict())


@app_views.route("/products/<product_id>", methods=["DELETE"],
                 strict_slashes=False)
@swag_from("api_docs/products/delete_product.yaml")
def delete_product(product_id):
    """ Deletes a product instance """
    product = storage.get(Product, product_id)

    if not product:
        abort(404)

    storage.delete(product)
    storage.save()

    return jsonify({}), 204


@app_views.route("/shops/<shop_id>/products", methods=["POST"],
                 strict_slashes=False)
@swag_from("api_docs/products/create_product.yaml")
def create_product(shop_id):
    """ Creates a product instance """
    shop = storage.get(Shop, shop_id)

    if not shop:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    category_id = data.get("category_id")

    if not category_id or not storage.get(Category, category_id):
        return jsonify({"error": "Invalid category_id"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    if "brand" not in data:
        return jsonify({"error": "Missing brand"}), 400

    if "price" not in data:
        return jsonify({"error": "Missing price"}), 400

    if "image" not in data:
        return jsonify({"error": "Missing image"}), 400

    data["shop_id"] = shop_id

    new_product = Product(**data)
    new_product.save()

    return jsonify(new_product.to_dict()), 201


@app_views.route("/products/<product_id>", methods=["PUT"],
                 strict_slashes=False)
@swag_from("api_docs/products/update_product.yaml")
def update_product(product_id):
    """ Updates a product instance """
    product = storage.get(Product, product_id)

    if not product:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = [
            'id',
            'shop_id',
            'category_id',
            'created_at',
            'updated_at'
            ]

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(product, key, value)

    storage.save()

    return jsonify(product.to_dict())


@app_views.route("/products/search", methods=["POST"],
                 strict_slashes=False)
@swag_from("api_docs/products/search_product.yaml")
def product_search():
    """ Retrive specific products based on search query """
    # Get search criteria from request body
    search_criteria = request.get_json()

    # Sorting parameters (with defaults)
    sort = search_criteria.get('sort', 'name')  # Default by product name
    order = search_criteria.get('order', 'asc')  # Default order ascending

    # Pagination parameters (with defaults)
    offset = search_criteria.get('offset', 0)
    limit = search_criteria.get('limit', 10)

    if not isinstance(offset, int) or not isinstance(limit, int):
        return jsonify({"error": "invalid limit or offset"}), 400

    # Add metadata like pagination to response
    query = storage.build_query()

    if 'name' in search_criteria:
        query = query.filter(
                Product.name.ilike(f"%{search_criteria['name']}%")
                )

    if 'min_price' in search_criteria:
        if not isinstance(search_criteria['min_price'], int):
            return jsonify({"error": "invalid min_price"}), 400

        query = query.filter(Product.price >= search_criteria['min_price'])

    if 'max_price' in search_criteria:
        if not isinstance(search_criteria['max_price'], int):
            return jsonify({"error": "invalid max_price"}), 400

        query = query.filter(Product.price <= search_criteria['max_price'])

    if 'brand' in search_criteria:
        query = query.filter(
                Product.brand.ilike(f"%{search_criteria['brand']}%")
                )

    if 'category_id' in search_criteria:
        query = query.filter(
                Product.category_id == search_criteria['category_id']
                )

    # Sorting logic
    if order == 'desc':
        query = query.order_by(getattr(Product, sort).desc())
    else:
        query = query.order_by(getattr(Product, sort).asc())

    # Pagination logic
        query = query.offset(offset).limit(limit)

    # Execute the query and fetch the results
    products = query.all()

    # Group results by shops
    shops = {}
    for product in products:
        shop = storage.get(Shop, product.shop_id)
        if shop.id not in shops:
            shops[shop.id] = {
                "shop_name": shop.name,
                "shop_id": shop.id,
                "products": []
            }
        shops[shop.id]["products"].append(product.to_dict())

    # Format the result as JSON
    result = list(shops.values())

    return jsonify({
        "products_count": query.count(),
        "offset": offset,
        "limit": limit,
        "shops": result
        })
