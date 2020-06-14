import os
import jwt
from functools import wraps
from flask import request
from models.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]

        if not token:
            return {'message': 'Token is missing!'}, 401

        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'))
            current_user = User.query.get(data['sub'])
        except:
            return {'message': 'Token is invalid!'}, 401

        return f(current_user, *args, **kwargs)

    return decorated
