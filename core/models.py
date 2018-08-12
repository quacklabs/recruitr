# from flask_sqlalchemy import SQLAlchemy
import datetime
from core import db, login_manager
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, current_user
from sqlalchemy.orm import scoped_session, sessionmaker



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True)
    phone = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    registered_on = db.Column(db.DateTime, default=datetime.datetime.now)
    account_type = db.Column(db.String(10))
    last_login = db.Column(db.DateTime, default=datetime.datetime.now)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def register_user(self, ):
        """
        Register a new user
        """
        return "ok"

class Verifications(db.Model):

    __tablename__ = "verifications"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(11))
    code = db.Column(db.String(8))
    status = db.Column(db.Boolean, default=False)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
