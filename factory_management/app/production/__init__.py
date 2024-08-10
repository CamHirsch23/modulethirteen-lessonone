from flask import Blueprint

bp = Blueprint('production', __name__)

from . import routes