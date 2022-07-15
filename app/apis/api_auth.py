from flask import request, abort, jsonify, url_for, g
from flask_restful import Api, Resource, fields, marshal_with, marshal, reqparse
#
from app.models.sqlite import User
from app.lib.myauth import my_login_password_required
from app.ext.cache import cache
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
                'duration': cache.config.get('CACHE_DEFAULT_TIMEOUT')
            }
        except:
            return {
                'code': 1,
                'msg': 'request token error'
            }
    
api_auth.add_resource(ResourceToken, '/token')


