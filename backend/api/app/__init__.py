from flask import Flask
from .core.config import Config
from .core.extensions import db, migrate, ma
from .domains.user.routes import user_bp
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    #app.config.from_object(Config)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    #app.register_blueprint(user_bp)

    return app