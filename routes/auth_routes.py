from flask import Blueprint, jsonify, request
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "no data sent"}), 400
    if "username" not in data:
        return jsonify({"error": "username is required"}), 400
    if "password" not in data:
        return jsonify({"error": "password is required"}), 400

    try:
        AuthService.create_user(data["username"], data["password"])
        return jsonify({"message": "user registered!"}), 201
    except:
        return jsonify({"error": "username already exists"}), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "no data sent"}), 400

    user = AuthService.find_user(data["username"])

    if not user:
        return jsonify({"error": "user not found"}), 404

    if AuthService.verify_password(data["password"], user["password"]):
        token = AuthService.generate_token(user["id"])
        return jsonify({"token": token}), 200

    return jsonify({"error": "wrong password"}), 401