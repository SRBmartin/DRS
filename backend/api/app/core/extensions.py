from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from ..application.Mediator import Mediator

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
m = Mediator()