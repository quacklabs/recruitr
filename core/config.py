import os
basedir = os.path.abspath(os.path.dirname(__file__))




sql_config = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
        username="root",
        password="root",
        hostname="127.0.0.1",
        databasename="recruitr_db",
    )
sql_config_test = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
        username="root",
        password="root",
        hostname="127.0.0.1",
        databasename="recruitr_db_test",
    )
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
    #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class BaseConfig:
    """Base configuration."""
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AUTH0_DOMAIN = 'quacklabs.eu.auth0.com'
    API_AUDIENCE = "https://recruitr.org/auth0/api"
    ALGORITHMS = ["RS256"]


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = sql_config


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = sql_config_test
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
