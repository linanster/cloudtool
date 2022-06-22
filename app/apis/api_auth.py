from flask import request, abort, jsonify, url_for, g
from flask_restful import Api, Resource, fields, marshal_with, marshal, reqparse
#
from app.models.sqlite import User
from app.lib.myauth import my_login_required
from app.ext.cache import cache
#
api_auth = Api(prefix='/api/auth/')

class ResourceToken(Resource):
    @my_login_required
    def get(self):
        token = g.user.generate_auth_token()
        return {
            'msg': 'auth success',
            'status': 202,
            'username':g.user.username,
            'token': token if type(token) is str else token.decode('ascii'),
            'duration': cache.config.get('CACHE_DEFAULT_TIMEOUT')
        }
    
api_auth.add_resource(ResourceToken, '/token')


