from flask import jsonify, request
from app import db, limiter
from app.models import Production
from . import bp

@bp.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def create_production():
    data = request.get_json()
    new_production = Production(product_id=data['product_id'], quantity_produced=data['quantity_produced'], date_produced=data['date_produced'])
    db.session.add(new_production)
    db.session.commit()
    return jsonify({'id': new_production.id}), 201

@bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
def get_productions():
    productions = Production.query.all()
    return jsonify([{'id': prod.id, 'product_id': prod.product_id, 'quantity_produced': prod.quantity_produced, 'date_produced': prod.date_produced} for prod in productions])