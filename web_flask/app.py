"""
Starts a flask web app
"""
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

@app.route("/grocery_list", strict_slashes=False)
def shop_list():
    """ Return grocery_list page """
    return render_template("grocery_list.html")

@app.route("/user_profile", strict_slashes=False)
def user_profile():
    """ Returns the user_profile page """
    return render_template("user_profile.html")

@app.route("/product_display", strict_slashes=False)
def product_display():
    """ Returns the product_display page"""
    return render_template("product_display.html")

@app.route("/product_search", strict_slashes=False)
def product_search():
    """ Return the product_search page """
    return render_template("product_search.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
