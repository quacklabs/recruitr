import os
from flask_script import Manager
from core import db, create_app
#config_name = os.getenv('FLASK_CONFIG')
app = create_app()


manager = Manager(app)



@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    #app.debug = True
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 8000))
    manager.run()
