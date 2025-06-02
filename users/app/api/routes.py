from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort
from flask import Response
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models.user import User
from app.utils import validate_payload

users_bp = Blueprint("users_bp", __name__, url_prefix="/api/users")


@users_bp.route("")
def get_all():
    users = db.session.execute(db.select(User)).scalars()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list), 200


@users_bp.route("/<int:id>", methods=["GET"])
def get_by_id(id):
    user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@users_bp.route("username/<string:username>", methods=["GET"])
def get_by_username(username):
    user = db.session.execute(
        db.select(User).filter_by(username=username)
    ).scalar_one_or_none()
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@users_bp.route("", methods=["POST"])
def insert():
    data = request.json
    validate_payload(data)
    pwd = generate_password_hash(data["password"])
    user = User(
        username=data["username"],
        password=pwd,
        role=data["role"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@users_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()
    if user is None:
        abort(404)
    data = request.json
    validate_payload(data)
    user.username = data["username"]
    user.password = generate_password_hash(data["password"])
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.role = data["role"]
    user.age = data["age"]
    db.session.commit()
    return jsonify(user.to_dict()), 200


@users_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return Response(status=200)
