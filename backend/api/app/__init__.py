from flask import Flask
from .core.config import Config
from .core.extensions import db, migrate, ma
from .presentation.user.routes import user_bp
from .presentation.survey.routes import survey_bp
import os
from flask_migrate import Migrate
from .application.mediator import initialize_mediator
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)

    CORS(app)

    migrations_dir = os.path.join(app.root_path, '..', 'app', 'Infrastructure', 'persistence', 'migrations')
    migrations_dir = os.path.abspath(migrations_dir)
    migrate = Migrate(app, db, directory=migrations_dir)

    mediator = initialize_mediator(app)
    app.config['mediator'] = mediator

    from .domains.user.models import User

    #TODO: Add all new routes blueprint when adding a new module
    app.register_blueprint(user_bp)
    app.register_blueprint(survey_bp)

    return app