from flask import request, jsonify, abort
from . import api
from flask_graphql import GraphQLView


@api.route("/generate_otp", methods=["POST"])
def generate_otp():
    from core.models import User, Verifications
    from core.utils import OTP as otp
    
    response = dict()
    if not request.json:
        abort(400)
    phone = request.json.get("phone")
    print(phone)
    phone_exists = User.query.filter_by(phone=phone).first()

    if phone_exists is None:
        response.update({"status": "ok", "message":"valid"})
        otp.generate_otp(phone)

    else:
        response.update({"status": "error", "message":"invalid"})


    return jsonify(response)

@api.route("/verify_otp", methods=["POST"])
def validate_otp():
    from core.utils import OTP as otp
    from core.models import Verifications as verify
    response = dict()
    phone = request.json.get('phone')
    code = request.json.get('code')
    code_valid = verify.query.filter_by(phone=phone, code=code, status="0").first()
    if code_valid is not None:
        response.update({"status":"ok", "message":"Valid Otp"})
        otp.cancel_code(phone, code)
    else:
        response.update({"status":"ok","message":"invalid code entered"})

    return jsonify(response)





@api.route("/register", methods=["POST"])
def response():
    text = { "message": "ok"}
    return jsonify(text)

