from flask import jsonify, request
from app import db, limiter
from app.models import Product
from . import bp

@bp.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'id': new_product.id}), 201

@bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
def get_products():
    products = Product.query.all()
    return jsonify([{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products])