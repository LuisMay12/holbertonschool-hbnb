from flask import Blueprint, jsonify
from app.services.hbnb_facade import HNBNBFacade

api_bp = Blueprint("api", __name__)
facade = HNBNBFacade()

@api_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "OK"})

@api_bp.route("/objects", methods=["GET"])
def list_objects():
    return jsonify(facade.list_all())