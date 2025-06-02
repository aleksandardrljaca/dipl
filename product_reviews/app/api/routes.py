from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort
from app.extensions import db
from app.models.review import Review
from app.utils import validate_data
from flask import Response

review_bp = Blueprint("reviews_bp", __name__, url_prefix="/api/product-reviews")


@review_bp.route("", methods=["GET"])
def get_all():
    reviews = db.session.execute(db.select(Review)).scalars()
    reviews_list = [review.to_dict() for review in reviews]
    return jsonify(reviews_list), 200


@review_bp.route("/<int:id>", methods=["GET"])
def get_all_by_product_id(id):
    reviews = db.session.execute(db.select(Review).filter_by(product_id=id)).scalars()
    reviews_list = [review.to_dict() for review in reviews]
    return jsonify(reviews_list), 200


@review_bp.route("", methods=["POST"])
def insert():
    body = request.json
    validate_data(body)
    review = Review(product_id=body["product_id"], review=body["review"])
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201


@review_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    review = db.session.execute(db.select(Review).filter_by(id=id)).scalar_one_or_none()
    if review is None:
        abort(404)
    body = request.json
    validate_data(body)
    review.product_id = body["product_id"]
    review.review = body["review"]
    db.session.commit()
    return jsonify(review.to_dict()), 200


@review_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    review = db.session.execute(db.select(Review).filter_by(id=id)).scalar_one_or_none()
    if review is None:
        abort(404)
    db.session.delete(review)
    db.session.commit()
    return Response(status=200)
