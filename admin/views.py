from flask import request, g
from flask_login import login_manager, login_required


from . import admin


@admin.route("/login", methods=["GET","POST"])
def login_admin():
    return ""
