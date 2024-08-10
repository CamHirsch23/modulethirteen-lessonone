from flask import Blueprint

bp = Blueprint('employee', __name__)

from . import routes