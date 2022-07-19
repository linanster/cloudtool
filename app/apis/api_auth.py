import traceback
from flask import request, abort, jsonify, url_for, g
from flask_restful import Api, Resource, fields, marshal_with, marshal, reqparse
#
from app.models.sqlite import User
from app.lib.myauth import my_login_password_required
from app.ext.cache import cache
from app.myglobals import cache_expiration
#
api_auth = Api(prefix='/api/auth/')

class ResourceToken(Resource):
    @my_login_password_required
    def post(self):
        try:
            token = g.user.generate_auth_token()
            return {
                'code': 0,
                'msg': 'request token success',
                'username':g.user.username,
                'token': token if type(token) is str else token.decode('ascii'),
                # 'duration': cache.config.get('CACHE_DEFAULT_TIMEOUT')
                'duration': cache_expiration
            }
        except Exception as e:
            traceback.print_exc()
            return {
                'code': 1,
                'msg': 'unknown error',
                'debug': str(e)
            }
    
api_auth.add_resource(ResourceToken, '/token')


