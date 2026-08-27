# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config=None):
    """Simple application factory — used by legacy tests (test_products, test_categories)."""
    app = Flask(__name__)

    # Default configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Override with provided config (e.g., for testing)
    if config:
        app.config.update(config)

    db.init_app(app)

    # Register legacy routes
    from app.routes import products_bp
    app.register_blueprint(products_bp)

    return app


def init_app(config_override=None):
    """
    Full application factory — registers all controllers, JWT, Flasgger, etc.
    Used by run.py and the new test suite (test_product, test_user, test_order, test_create_order).
    """
    from flask_jwt_extended import JWTManager
    from app.config import Config

    app = Flask(__name__)
    app.config.from_object(Config)

    # Override with test config if provided
    if config_override:
        app.config.update(config_override)

    db.init_app(app)
    JWTManager(app)

    # Try to register Flasgger (optional, not required for tests)
    try:
        from flasgger import Swagger
        Swagger(app, template=app.config.get('SWAGGER_TEMPLATE', {}))
    except ImportError:
        pass

    # Register controllers (blueprints)
    from app.controllers import products_bp, users_bp, orders_bp, auth_bp
    app.register_blueprint(products_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(auth_bp)

    # Register error handlers
    from app.middleware.errors import register_error_handlers
    register_error_handlers(app)

    return app
