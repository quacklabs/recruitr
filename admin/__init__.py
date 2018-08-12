from flask import Blueprint
# from core.models import User
admin = Blueprint('admin', __name__)

from . import views
