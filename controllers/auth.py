from os import getenv
import jwt
import datetime
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from app import db, mail
from models.models import User
from models.schemas import UserSchema
from middlewares.auth import token_required

auth_module = Blueprint('auth', __name__)


# @desc      Login user
# @route     POST /api/v1/auth/login
# @access    Public
@auth_module.route('/login', methods=['POST'])
def login():
    data = request.json

    if not data or not data['email'] or not data['password']:
        return {'success': False, 'error': 'invalid credentials'}, 401

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        # return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        return {'success': False, 'error': 'invalid credentials'}, 401

    if check_password_hash(user.password, data['password']):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30, seconds=30),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id
        }
        token = jwt.encode(payload, getenv('SECRET_KEY'), algorithm='HS256')

        return {'success': True, 'token': token.decode('UTF-8')}, 200

    return {'success': False, 'error': 'invalid credentials'}, 401


# @desc      Current user
# @route     GET /api/v1/auth/get_current_user
# @access    Private
@auth_module.route('/get_current_user', methods=['GET'])
@token_required
def get_current_user(current_user):
    user_schema = UserSchema()
    user_data = user_schema.dump(current_user)
    return {'success': True, 'data': user_data}, 200


