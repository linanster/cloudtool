from flask import request, session, g
from flask_restful import abort
from functools import wraps
#
from app.models.sqlite import User
from app.ext.cache import cache
#
# this is decorator
def my_login_password_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        username = request.json.get('username')
        password = request.json.get('password')

        user = User.query.filter_by(username = username).first()
        if not user:
            abort(401, code = 1, msg = 'error: user not found')
        if not user.verify_password(password):
            abort(401, code = 2, msg = 'error: invalid password')
        g.user = user
        return func(*args, **kwargs)
    return inner

def my_login_token_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        token = request.headers.get('access_token')
        user = User.verify_auth_token(token)
        if not user:
            abort(401, code = 3, msg = 'error: token invalid or expired')
        #### code for single login restriction ####
        token_latest = cache.get(str(user.id))
        if token != token_latest:
            abort(401, code = 4, msg = 'error: token refreshed by other side')
        ########
        g.user = user
        return func(*args, **kwargs)
    return inner

def my_login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        token = request.headers.get('access_token')
        username = request.headers.get('username') or request.json.get('username') if request.json else None
        password = request.headers.get('password') or request.json.get('password') if request.json else None

        # 1. first try to authenticate by token
        user = User.verify_auth_token(token)
        if not user:
            # 2. try to authenticate with username/password
            user = User.query.filter_by(username = username).first()
            if not user or not user.verify_password(password):
                abort(401, code = 401, msg = 'authentication failed')
        g.user = user
        return func(*args, **kwargs)
    return inner

def my_permission_required(required_permission):
    def inner1(func):
        def inner2(*args, **kwargs):
            if not g.user.check_permission(required_permission):
                abort(403, code = 5, msg = 'error: permission not sufficient')
            return func(*args, **kwargs)
        return inner2
    return inner1
