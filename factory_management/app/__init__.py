from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    limiter.init_app(app)

    from .employee import bp as employee_bp
    app.register_blueprint(employee_bp, url_prefix='/employees')

    from .product import bp as product_bp
    app.register_blueprint(product_bp, url_prefix='/products')

    from .order import bp as order_bp
    app.register_blueprint(order_bp, url_prefix='/orders')

    from .customer import bp as customer_bp
    app.register_blueprint(customer_bp, url_prefix='/customers')

    from .production import bp as production_bp
    app.register_blueprint(production_bp, url_prefix='/production')

    return app