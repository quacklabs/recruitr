from flask import Blueprint
# from core.models import User
api = Blueprint('api', __name__)

from . import views
