# from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
from core import db, login_manager
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, current_user
from flask import current_app as app
from sqlalchemy.orm import scoped_session, sessionmaker

#db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db))

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

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user
    
    
    # def verify_password(self, password):
    #     """
    #     Check if hashed password matches actual password
    #     """
    #     return check_password_hash(self.password_hash, password)

    # def __init__(self,password):
    #     self.email = email
    #     self.phone = phone
    #     self.password = generate_password_hash(
    #         password, app_settings.get('BCRYPT_LOG_ROUNDS')
    #     ).decode()
    #     self.registered_on = datetime.datetime.now()
        

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config['SECRET_KEY'])
            #is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            # if is_blacklisted_token:
            #     return 'Token blacklisted. Please log in again.'
            # else:
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

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
