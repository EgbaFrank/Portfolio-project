"""
Flask API implementation
"""
from os import getenv
from models import storage
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from flasgger import Swagger


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

app.config['SWAGGER'] = {
        'title': 'Grocery Hub API',
        'description': 'API for Grocery Hub',
        'uiversion': 3
}

Swagger(app)


@app.teardown_appcontext
def close_storage(exception):
    """Cleans up resources after each request"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handles 404 - Not Found Error
    ---
    responses:
        404:
            description: The resource was not found
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('GH_API_HOST', '0.0.0.0')
    port = int(getenv('GH_API_PORT', '5000'))

    app.run(host=host, port=port, threaded=True)
