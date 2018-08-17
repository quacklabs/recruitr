import os
import pymysql
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from flask_cors import CORS
from flask_jwt import JWT
#from flask_graphql import GraphQLView


class FrontEnd(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='[[',
        variable_end_string=']]',
        comment_start_string='{#',
        comment_end_string='#}',
    ))


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()
jwt = JWT()


def create_app():
    
    app = FrontEnd(__name__)
    app_settings = os.getenv(
        'APP_SETTINGS',
        'core.config.DevelopmentConfig'
    )
    app.config.from_object(app_settings)
    app.debug = True
    jwt.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "admin.login"
    login_manager.session_protection = "strong"
    migrate = Migrate(app, db)
    moment.init_app(app)

    #from core import models

    # from .admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint, url_prefix='/admin')
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)
    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    from api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")
    csrf.exempt(api_blueprint)

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/backend")
    #from employer import employer as employer_blueprint
    #app.register_blueprint(employer_blueprint)
    return app
