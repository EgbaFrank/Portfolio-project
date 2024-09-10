"""
Starts a flask web app
"""
from os import getenv
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def close_db(execption):
    """ Close current db session """
    storage.close()


@app.route("/", strict_slashes=False)
def login():
    """ Returns the login page """
    return render_template("index.html")


@app.route("/grocery_list/<list_id>", strict_slashes=False)
def shop_list(list_id=None):
    """ Return grocery_list page """
    from models.shop_list import Shop_list
    user_list = storage.get(Shop_list, list_id)
    return render_template(
            "grocery_list.html",
            user_list=user_list
            )


@app.route("/user_profile", strict_slashes=False)
def user_profile():
    """ Returns the user_profile page """
    return render_template("user_profile.html")


@app.route("/product_display", strict_slashes=False)
def product_display():
    """ Returns the product_display page"""
    from models.category import Category
    categories = storage.all(Category).values()
    return render_template(
            "product_display.html",
            categories=categories
            )


@app.route("/product_search", strict_slashes=False)
def product_search():
    """ Return the product_search page """
    from models.shop import Shop
    shops = storage.all(Shop).values()
    return render_template(
            "product_search.html",
            shops=shops
            )

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))

    app.run(host=host, port=port, threaded=True)
