from os import getenv
import jwt
import datetime
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models.models import User
from models.schemas import UserSchema
from middlewares.auth import token_required
from utils.send_mail import send_mail

auth_module = Blueprint('auth', __name__)


# ======================================================================================
# @desc      Login user
# @route     POST /api/v1/auth/login
# @access    Public
# ======================================================================================
@auth_module.route('/login', methods=['POST'])
def login():
    data = request.json

    if not data or not data['email'] or not data['password']:
        return {'success': False, 'error': 'invalid credentials'}, 401

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        # return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        return {'success': False, 'error': 'invalid credentials'}, 401

    if not user.verified_at:
        # return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        return {'success': False, 'error': 'Email not verified'}, 401

    if check_password_hash(user.password, data['password']):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30, seconds=30),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id
        }
        token = jwt.encode(payload, getenv('SECRET_KEY'), algorithm='HS256').decode('UTF-8')

        return {'success': True, 'token': token}, 200

    return {'success': False, 'error': 'invalid credentials'}, 401


# ======================================================================================
# @desc      Register user
# @route     POST /api/v1/auth/register
# @access    Public
# ======================================================================================
@auth_module.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name'] if 'name' in data else None
    email = data['email'] if 'email' in data else None
    password = data['password'] if 'password' in data else None

    # Validate
    if not email or not password:
        return {'success': False, 'error': 'Email & Password Required'}, 401

    # Hash Password
    hashed_password = generate_password_hash(password, method='sha256')

    # If user exists
    user = User.query.filter_by(email=email).first()
    if user:
        return {'success': False, 'error': 'User already exists'}, 401

    # Create user
    new_usr = User(username=name, email=email, password=hashed_password)

    # Send verification email with token
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30, seconds=30),
            'iat': datetime.datetime.utcnow(),
            'sub': email
        }
        email_token = jwt.encode(payload, getenv('SECRET_KEY'), algorithm='HS256').decode('UTF-8')
        verify_url = f"http://{getenv('FLASK_RUN_HOST')}:{getenv('FLASK_RUN_PORT')}/api/v1/auth/verify_email/{email_token}"

        subject = "flask-app Verify Email"
        message = (f'<div style="text-align: center; padding: 20px; line-height: 2; font-size: 1.2rem">'
                   f'You have Registered successfully. <br /> Visit the following link to verify your email and continue to login <br /><br />'
                   f'<a href="{verify_url}" style="background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 1rem; font-weight: bold">'
                   f'VERIFY EMAIL'
                   f'</a>'
                   f'<p style="color: red;">This link will expire shortly</p>'
                   f'</div>')
        send_mail(email, subject, message)

    except Exception as e:
        print('\x1b[91m' + str(e) + '\x1b[0m')
        return {'success': False, 'error': 'Sending Email Failed'}, 500

    # save user into DB
    db.session.add(new_usr)
    db.session.commit()
    return {'success': True, 'data': 'Verification Email sent'}, 200


# ======================================================================================
# @desc      Verify Email
# @route     GET /api/v1/auth/verify_email/<token>
# @access    Public
# ======================================================================================
@auth_module.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    payload = jwt.decode(token, getenv('SECRET_KEY'))
    user = User.query.filter_by(email=payload['sub']).first()
    user.verified_at = datetime.datetime.utcnow()
    db.session.commit()
    return {'success': True, 'data': "Email Verified"}, 200


# ======================================================================================
# @desc      Forgot Password
# @route     POST /api/v1/auth/forgot_password
# @access    Public
# ======================================================================================
@auth_module.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data['email'] if 'email' in data else None

    # Validate
    if not email:
        return {'success': False, 'error': 'Email is Required'}, 401

    # If user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return {'success': False, 'error': "User doesn't exist"}, 401

    # Send email with Reset token
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30, seconds=30),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id
        }
        reset_token = jwt.encode(payload, getenv('SECRET_KEY'), algorithm='HS256').decode('UTF-8')
        reset_url = f"http://{getenv('FLASK_RUN_HOST')}:{getenv('FLASK_RUN_PORT')}/api/v1/auth/reset_password/{reset_token}"

        subject = "Reset Password - flask-app"
        message = (f'<div style="text-align: center; padding: 20px; line-height: 2; font-size: 1.2rem">'
                   f'You are receiving this email because you (or someone else) have requested to reset a password. <br /> Make a PUT request to the following link to reset your password <br /><br />'
                   f'<a href="{reset_url}" style="background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 1rem; font-weight: bold">'
                   f'RESET PASSWORD'
                   f'</a>'
                   f'<p style="color: red;">This link will expire shortly</p>'
                   f'</div>')
        send_mail(email, subject, message)

    except Exception as e:
        print('\x1b[91m' + str(e) + '\x1b[0m')
        return {'success': False, 'error': 'Sending Email Failed'}, 500

    return {'success': True, 'data': "Password Reset Email Sent"}, 200


# ======================================================================================
# @desc      Reset Password
# @route     PUT /api/v1/auth/reset_password/<token>
# @access    Public
# ======================================================================================
@auth_module.route('/reset_password/<token>', methods=['PUT'])
def reset_password(token):
    # Get Token
    if not token:
        return {'success': False, 'error': 'Token is missing!'}, 401

    try:
        payload = jwt.decode(token, getenv('SECRET_KEY'))
        user = User.query.get(payload['sub'])
    except:
        return {'success': False, 'error': 'Token is invalid!'}, 401

    # Get Password
    data, password = None, None
    try:
        data = request.json
        password = data['password'] if 'password' in data else None
    except:
        pass

    # Validate
    if not data or password:
        return {'success': False, 'error': 'Password is Required'}, 401

    # Hash Password
    hashed_password = generate_password_hash(password, method='sha256')

    # update user
    user.password = hashed_password
    db.session.commit()

    return {'success': True, 'data': "Password Reset Successful"}, 200


# ======================================================================================
# @desc      Current user
# @route     GET /api/v1/auth/get_current_user
# @access    Private
# ======================================================================================
@auth_module.route('/get_current_user', methods=['GET'])
@token_required
def get_current_user(current_user):
    user_schema = UserSchema()
    user_data = user_schema.dump(current_user)
    return {'success': True, 'data': user_data}, 200

