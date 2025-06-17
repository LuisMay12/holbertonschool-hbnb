from flask import Blueprint, jsonify
from app.services.hbnb_facade import HBNBFacade

api_bp = Blueprint("api", __name__)
facade = HBNBFacade()

@api_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "OK"})

@api_bp.route("/objects", methods=["GET"])
def list_objects():
    return jsonify(facade.list_all())