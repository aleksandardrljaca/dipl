from flask import request
from flask import jsonify
from flask import Blueprint
from flask import Response
from app.models.category import Category
from app.extensions import db
from app.utils import validate_payload
from app.security.decorators import admin_required
from flask import abort

categories_bp = Blueprint("categories_bp", __name__, url_prefix="/api/categories")


@categories_bp.route("", methods=["GET"])
def get_all():
    categories = db.session.execute(db.select(Category)).scalars()
    categories_list = [category.to_dict() for category in categories]
    return jsonify(categories_list), 200


@categories_bp.route("/<int:id>", methods=["GET"])
def get_by_id(id):
    category = db.session.execute(
        db.select(Category).filter_by(id=id)
    ).scalar_one_or_none()
    if category is None:
        abort(404)
    return jsonify(category.to_dict()), 200


@categories_bp.route("", methods=["POST"])
@admin_required()
def insert():
    data = request.json
    validate_payload(data)
    category = Category(name=data["name"], description=data["description"])
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@categories_bp.route("/<int:id>", methods=["PUT"])
@admin_required()
def update(id):
    category = db.session.execute(
        db.select(Category).filter_by(id=id)
    ).scalar_one_or_none()
    if category is None:
        abort(404)
    data = request.json
    validate_payload(data)
    category.name = data["name"]
    category.description = data["description"]
    db.session.commit()
    return jsonify(category.to_dict()), 200


@categories_bp.route("/<int:id>", methods=["DELETE"])
@admin_required()
def delete(id):
    category = db.session.execute(
        db.select(Category).filter_by(id=id)
    ).scalar_one_or_none()
    if category is None:
        abort(404)
    db.session.delete(category)
    db.session.commit()
    return Response(status=200)
