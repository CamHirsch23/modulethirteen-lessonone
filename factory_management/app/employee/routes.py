from flask import jsonify, request
from app import db, limiter
from app.models import Employee
from . import bp

@bp.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def create_employee():
    data = request.get_json()
    new_employee = Employee(name=data['name'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id}), 201

@bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees])