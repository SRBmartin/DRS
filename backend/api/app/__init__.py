from flask import Flask
from .core.config import Config
from .core.extensions import db, migrate, ma
from .domains.user.routes import user_bp
import os
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)

    migrations_dir = os.path.join(app.root_path, '..', 'app', 'Infrastructure', 'persistence', 'migrations')
    migrations_dir = os.path.abspath(migrations_dir)
    migrate = Migrate(app, db, directory=migrations_dir)

    from .domains.user.models import User

    app.register_blueprint(user_bp)

    return app