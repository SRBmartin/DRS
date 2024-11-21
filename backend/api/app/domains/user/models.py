import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime, timedelta
from ...core.extensions import db
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'users'}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<User {self.name} {self.lastname}>'
    
    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password = hashed_password.decode('utf-8')

    def check_password(self, password: str):
        hashed_password = self.password.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    
class Session(db.Model):
    __tablename__ = "session"
    __table_args__ = {'schema': 'users'}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.users.id'), nullable=False)
    started_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ending_time = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=2), nullable=True)
    ip_address = db.Column(db.String(45), nullable=False)

    user = relationship("User", backref=db.backref("sessions", lazy=True))