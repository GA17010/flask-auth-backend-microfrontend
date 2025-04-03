from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config
from app.database import db

migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={r"/auth/*": {"origins": app.config['CORS_ORIGINS'], "supports_credentials": True}})
    CORS(app, resources={r"/recovery/*": {"origins": app.config['CORS_ORIGINS'], "supports_credentials": True}})
    CORS(app, resources={r"/user/*": {"origins": app.config['CORS_ORIGINS'], "supports_credentials": True}})

    from .routes.auth_routes import auth_bp
    from .routes.user_routes import user_bp
    from .routes.recovery_routes import recovery_bp
    from .models import user_model

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(recovery_bp, url_prefix="/recovery")
    app.register_blueprint(user_bp, url_prefix="/user")

    return app