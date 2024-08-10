from flask import jsonify, request
from app import db, limiter
from app.models import Customer
from . import bp

@bp.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def create_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'id': new_customer.id}), 201

@bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': cust.id, 'name': cust.name, 'email': cust.email, 'phone': cust.phone} for cust in customers])