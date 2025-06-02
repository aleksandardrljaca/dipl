from flask import Blueprint
from flask import request
from flask import abort
from flask import Response
from app.models.product import Product
from app.utils import validate_data
from app.security.decorators import admin_required
from flask import jsonify
from app.extensions import db

products_bp = Blueprint("products_bp", __name__, url_prefix="/api/products")


@products_bp.route("")
def get_all():
    products = db.session.execute(db.select(Product)).scalars()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200


@products_bp.route("category/<int:id>")
def get_all_by_category_id(id):
    products = db.session.execute(
        db.select(Product).filter_by(category_id=id)
    ).scalars()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200


@products_bp.route("/<int:id>")
def get_by_id(id):
    product = db.session.execute(
        db.select(Product).filter_by(id=id)
    ).scalar_one_or_none()
    if product is None:
        abort(404)
    return jsonify(product.to_dict()), 200


@products_bp.route("", methods=["POST"])
@admin_required()
def insert():
    data = request.json
    validate_data(data)
    product = Product(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        category_id=data["category_id"],
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


@products_bp.route("/<int:id>", methods=["PUT"])
@admin_required()
def update(id):
    product = db.session.execute(
        db.select(Product).filter_by(id=id)
    ).scalar_one_or_none()
    if product is None:
        abort(400)
    data = request.json
    validate_data(data)
    product.name = data["name"]
    product.description = data["description"]
    product.price = data["price"]
    product.category_id = data["category_id"]
    db.session.commit()
    return jsonify(product.to_dict()), 200


@products_bp.route("/<int:id>", methods=["DELETE"])
@admin_required()
def delete(id):
    product = db.session.execute(
        db.select(Product).filter_by(id=id)
    ).scalar_one_or_none()
    if product is None:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    return Response(status=200)


@products_bp.route("/ids", methods=["POST"])
def get_ids():
    data = request.json
    ids = [item["id"] for item in data]
    products = []
    for product_id in ids:
        product = db.session.execute(
            db.select(Product).filter_by(id=int(product_id))
        ).scalar_one_or_none()
        if product:
            products.append(product)
    return jsonify([p.to_dict() for p in products]), 200
