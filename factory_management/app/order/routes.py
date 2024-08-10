from flask import jsonify, request
from app import db, limiter
from app.models import Order
from . import bp

@bp.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def create_order():
    data = request.get_json()
    new_order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'], total_price=data['total_price'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'id': new_order.id}), 201

@bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': order.id, 'customer_id': order.customer_id, 'product_id': order.product_id, 'quantity': order.quantity, 'total_price': order.total_price} for order in orders])