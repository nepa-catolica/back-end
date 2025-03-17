from datetime import timedelta

from flask import Flask
from dotenv import load_dotenv
from src.utils.extensions import db, jwt, migrate, ma
from flask_cors import CORS
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    from .routes.auth import bp as auth_bp
    from .routes.admin import bp as admin_bp
    from .routes.projetos import bp as projetos_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(projetos_bp, url_prefix='/projetos')

    return app
