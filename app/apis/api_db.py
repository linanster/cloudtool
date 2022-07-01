import traceback
from datetime import datetime
from flask import request, abort
from flask_restful import Api, Resource, fields, marshal_with, marshal, reqparse
from sqlalchemy import and_
#
from app.models.mysql import ToolRecord
from app.lib.myauth import my_login_required
#
api_db = Api(prefix='/api/db/')


#####################################################################
### 1.1 fields definition, for marshal (custom object serializing) ###
#####################################################################

fields_toolrecord_db = {
    'id': fields.Integer,
    'card_date': fields.DateTime(dt_format='iso8601'),
    'create_time': fields.DateTime(dt_format='iso8601'),
    'update_time': fields.DateTime(dt_format='iso8601'),
    'typecode': fields.Integer,
    'content': fields.String
}

fields_toolrecord_response = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(fields_toolrecord_db)
}

fields_toolrecords_response = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(fields_toolrecord_db))
}


#################################
### 1.2 parser initialization ###
#################################

parser = reqparse.RequestParser()
parser.add_argument('card_date', type=str, required=False, help='card_date required', location=['form', 'args', 'json'])
parser.add_argument('card_date_start', type=str, required=False, help='card_date_start required', location=['form', 'args', 'json'])
parser.add_argument('card_date_end', type=str, required=False, help='card_date_end required', location=['form', 'args', 'json'])
parser.add_argument('typecode', type=int, required=False, help='typecode required', location=['form', 'args'])
parser.add_argument('content', type=str, required=False, help='content required', location=['form', 'args'])

####################################
### 2. resource class definition ###
####################################


class ResourceToolRecord(Resource):

    @marshal_with(fields_toolrecord_response)
    @my_login_required
    def get(self, id):
        try:
            item = ToolRecord.query.get(id)
            if item:
                response = {
                    'code': 0,
                    'msg': 'query single record success',
                    'data': item
                }
            else:
                response = {
                    'code': 1,
                    'msg': 'query single record error(no record)',
                    'data': None
                }
        except:
            response = {
                'code': 1,
                'msg': 'query single record error',
                'data': None,
            }
            traceback.print_exc()
        return response

    @marshal_with(fields_toolrecord_response)
    @my_login_required
    def post(self):
        try:
            args = parser.parse_args()
            card_date = args.get('card_date') or request.json.get('card_date')
            typecode = args.get('typecode') or request.json.get('typecode')
            content = args.get('content') or request.json.get('content')
            create_time = datetime.now()
            update_time = datetime.now()
            item = ToolRecord.query.filter(ToolRecord.card_date == card_date).first()
            if item is not None:
                response = {
                    'code': 1,
                    'msg': 'insert record error (alreay exists)',
                    'data': item,
                }
            else:
                item = ToolRecord(card_date, create_time, update_time, typecode, content)
                item.save()
                response = {
                    'code': 0,
                    'msg': 'insert record success',
                    'data': item,
                }
        except:
            response = {
                'code': 1,
                'msg': 'insert record error',
                'data': None,
            }
            traceback.print_exc()
        return response
        
    @marshal_with(fields_toolrecord_response)
    @my_login_required
    def put(self, id):
        try:
            args = parser.parse_args()
            typecode = args.get('typecode') or request.json.get('typecode')
            content = args.get('content') or request.json.get('content')
            item = ToolRecord.query.get(id)
            update_time = datetime.now()
            item.typecode = typecode
            item.update_time = update_time
            item.content = content
            item.save()
            response = {
                'code': 0,
                'msg': 'update record success',
                'data': item,
            }
        except:
            response = {
                'code': 1,
                'msg': 'update record error',
                'data': None
            }
            traceback.print_exc()
        return response

    @marshal_with(fields_toolrecord_response)
    @my_login_required
    def delete(self, id):
        try:
            item = ToolRecord.query.get(id)
            item.delete()
            response = {
                'code': 0,
                'msg': 'delete record success',
                'data': item,
            }
        except:
            response = {
                'code': 1,
                'msg': 'delete record error',
                'data': None,
            }
            traceback.print_exc()
        return response

class ResourceToolRecords(Resource):

    @marshal_with(fields_toolrecords_response)
    @my_login_required
    def get(self):
        try:
            args = parser.parse_args()
            card_date_start = args.get('card_date_start')
            card_date_end = args.get('card_date_end')
            items = ToolRecord.query.filter(and_(ToolRecord.card_date >= card_date_start, ToolRecord.card_date <= card_date_end))
            response = {
                'code': 0,
                'msg': 'query multi records success',
                'data': items,
            }
        except:
            response = {
                'code': 1,
                'msg': 'query multi records error',
                'data': None,
            }
            traceback.print_exc()
        return response

##############################
### 3. Resourceful Routing ###
##############################

api_db.add_resource(ResourceToolRecord, '/toolrecord/', '/toolrecord/<id>')
api_db.add_resource(ResourceToolRecords, '/toolrecords/')

