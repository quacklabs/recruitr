from flask import request, jsonify, abort, make_response, current_app as app
from flask_jwt import JWT, jwt_required, current_identity
from core import db
from . import api
#from flask_graphql import GraphQLView
from core.models import User
@api.route("/", methods=["GET"])
@jwt_required()
def announce():
    data = {"data":"Welcome To Recruitr API", "ID" : current_identity}
    return jsonify(data)


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
def register_user():
    user_data = request.get_json()
    user = User.query.filter_by(email=user_data.get('email')).first()
    if not user:
        try:
            #Set data to be entered into the user's table
            user = User(
                email=user_data.get('email'),
                password=user_data.get('password'),
                phone=user_data.get('phone')
            )
            #insert the data
            db.session.add(user)
            db.session.commit()
            
            # generate JWT token
            auth_token = user.encode_auth_token(user.id)
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return make_response(jsonify(responseObject)), 201

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
        
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

