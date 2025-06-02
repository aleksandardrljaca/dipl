from flask import Blueprint
from flask import Response
from flask import jsonify
from flask import request
from flask import abort
import requests
from app.extensions import db
from app.models.order import Order, OrderProduct
from app.utils import validate_data

orders_bp = Blueprint("orders_bp", __name__, url_prefix="/api/orders")


@orders_bp.route("", methods=["GET"])
def get_all():
    orders = db.session.execute(db.select(Order)).scalars()
    orders_list = [order.to_dict() for order in orders]
    return jsonify(orders_list), 200


@orders_bp.route("/<int:id>", methods=["GET"])
def get_by_id(id):
    order = db.session.execute(db.select(Order).filter_by(id=id)).scalar_one_or_none()
    if order is None:
        abort(404)
    return jsonify(order.to_dict()), 200


@orders_bp.route("", methods=["POST"])
def insert():
    body = request.json
    product_response = requests.post(
        "https://localhost:8080/api/products/ids",
        headers=request.headers,
        json=body,
        verify="cert.crt",
    )
    if product_response.status_code != 200:
        return jsonify({"error": "Failed to fetch product details"}), 400

    products = product_response.json()
    validate_data(body)
    order = Order(total_price=0.0)
    db.session.add(order)
    db.session.flush()

    total_price = 0.0
    for item in body:
        product_id = item["id"]
        quantity = item["quantity"]

        p = next((x for x in products if x["id"] == product_id), None)
        if not p:
            continue

        order_product = OrderProduct(
            order_id=order.id,
            product_id=product_id,
            product_name=p["name"],
            quantity=quantity,
            unit_price=p["price"],
            order=order,
        )

        db.session.add(order_product)
        total_price += p["price"] * quantity

    order.total_price = total_price
    db.session.commit()

    return jsonify(order.to_dict()), 201


@orders_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    order = db.session.execute(db.select(Order).filter_by(id=id)).scalar_one_or_none()
    if order is None:
        abort(404)
    orderProducts = db.session.execute(
        db.select(OrderProduct).filter_by(order_id=id)
    ).scalars()
    for op in orderProducts:
        db.session.delete(op)
    db.session.delete(order)
    db.session.commit()
    return Response(status=200)
