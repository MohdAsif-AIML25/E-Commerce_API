import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from config import config_by_name

# Initialize extensions
db = SQLAlchemy()
flask_bcrypt = Bcrypt()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'dev')
    
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Register extensions
    db.init_app(app)
    flask_bcrypt.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register Blueprints (Routes) will be added here
    from app.routes.auth_routes import auth_blueprint
    from app.routes.product_routes import product_blueprint
    from app.routes.order_routes import order_blueprint
    from app.routes.payment_routes import payment_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(product_blueprint, url_prefix='/api/products')
    app.register_blueprint(order_blueprint, url_prefix='/api/orders')
    app.register_blueprint(payment_blueprint, url_prefix='/api/payments')

    return app
