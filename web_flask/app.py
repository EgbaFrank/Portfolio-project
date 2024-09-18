"""
Starts a flask web app
"""
from os import getenv
from flask import Flask, render_template
from models import storage
from uuid import uuid4

app = Flask(__name__)


@app.teardown_appcontext
def close_db(execption):
    """ Close current db session """
    storage.close()


@app.route("/", strict_slashes=False)
def home():
    """ Returns the home page """
    return render_template(
            "index.html",
            cache_id=uuid4()
            )


@app.route("/login", strict_slashes=False)
def login():
    """ Returns the home page """
    return render_template(
            "login.html",
            cache_id=uuid4()
            )


@app.route("/orders", strict_slashes=False)
def orders():
    """ Returns the order page """
    from models.user import User
    user_id = "dde51e22-a2e3-4425-9c1e-f77691f9c781"
    user = storage.get(User, user_id)
    return render_template("orders.html",
            orders=user.orders,
            cache_id=uuid4()
            )


@app.route("/grocery_list", strict_slashes=False)
def shop_list():
    """ Return grocery_list page """
    from models.user import User
    user_id = "dde51e22-a2e3-4425-9c1e-f77691f9c781"
    user = storage.get(User, user_id)
    return render_template(
            "grocery_list.html",
            user_list=user.shop_lists[0],
            cache_id=uuid4()
            )


@app.route("/user_profile", strict_slashes=False)
def user_profile():
    """ Returns the user_profile page """
    from models.user import User
    user_id = "dde51e22-a2e3-4425-9c1e-f77691f9c781"
    user = storage.get(User, user_id)

    return render_template(
            "user_profile.html",
            user=user,
            cache_id=uuid4() 
            )


@app.route("/product_display", strict_slashes=False)
def product_display():
    """ Returns the product_display page"""
    from models.category import Category
    categories = storage.all(Category).values()
    return render_template(
            "product_display.html",
            categories=categories,
            cache_id=uuid4()
            )


@app.route("/product_search", strict_slashes=False)
def product_search():
    """ Return the product_search page """
    from models.shop import Shop
    shops = storage.all(Shop).values()
    return render_template(
            "product_search.html",
            shops=shops,
            cache_id=uuid4()
            )


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))

    app.run(host=host, port=port, threaded=True)
