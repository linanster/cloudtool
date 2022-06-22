from flask import request, session, g
from flask_restful import abort
from functools import wraps
#
from app.models.sqlite import User
#
# this is decorator
def my_login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        username = request.form.get('username') or request.args.get('username') or request.headers.get('username')
        password = request.form.get('password') or request.args.get('password') or request.headers.get('password')
        token = request.form.get('token') or request.args.get('token') or request.headers.get('token')

        # 1. first try to authenticate by token
        user = User.verify_auth_token(token)
        if not user:
            # 2. try to authenticate with username/password
            user = User.query.filter_by(username = username).first()
            if not user or not user.verify_password(password):
                abort(401, status='401', msg='authentication failed')
        g.user = user
        return func(*args, **kwargs)
    return inner

