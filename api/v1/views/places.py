"""
RESTFul API actions for Places
"""
from models.place import Place
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/places", strict_slashes=False)
@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place(place_id=None):
    """Retrieves all or a specific place"""
    if not place_id:
        places = storage.all(Place).values()
        places_list = [place.to_dict() for place in places]

        return jsonify(places_list)

    else:
        place = storage.get(Place, place_id)

        if not place:
            abort(404)

        return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
        strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 204


@app_views.route("/places", methods=["POST"],
        strict_slashes=False)
def create_place():
    """ Creates a place instance """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(**data)
    new_place.save()

    return jsonify(new_place.to_dict()), 201

@app_views.route("/places/<place_id>", methods=["PUT"],
        strict_slashes=False)
def update_place(place_id):
    """ Updates a place instance """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict())

