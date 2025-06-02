from flask import Blueprint
from flask import request
from flask import Response
from flask import jsonify
import requests
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash
from app.utils import forward_request, validate_payload
from app.extensions import db
from app.models.token_blocklist import TokenBlocklist
from app.extensions import jwt
from datetime import datetime, timezone
from flask_jwt_extended import decode_token

gateway_bp = Blueprint("gateway_bp", __name__)


@gateway_bp.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required()
def route_to(path):
    return forward_request(path, request)


@gateway_bp.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@gateway_bp.route("/api/login", methods=["POST"])
def login():
    payload = request.json
    validate_payload(payload)
    username = payload["username"]
    response = requests.get(
        f"https://localhost:8084/api/users/username/{username}", verify="cert.crt"
    )
    if response.status_code != 200:
        return Response(status=response.status_code)
    user = response.json()
    if not check_password_hash(user["password"], payload["password"]):
        return Response(status=401)
    refresh_token = create_refresh_token(identity="user.username")
    decoded_refresh_token = decode_token(refresh_token)
    print(f"type {type(refresh_token)}")
    access_token = create_access_token(
        identity="user.username",
        additional_claims={
            "role": user["role"],
            "jti_refresh": decoded_refresh_token["jti"],
        },
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@gateway_bp.route("/api/logout", methods=["DELETE"])
@jwt_required()
def logout():
    token = get_jwt()
    jti_access_token = token["jti"]
    jti_refresh_token = token["jti_refresh"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti_access_token, created_at=now))
    db.session.add(TokenBlocklist(jti=jti_refresh_token, created_at=now))
    db.session.commit()
    return Response(status=200)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None
