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
    'date_time': fields.DateTime(dt_format='iso8601'),
    'colorcode': fields.Integer,
    'content': fields.String
}

fields_toolrecord_response = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(fields_toolrecord_db)
}

fields_toolrecords_response = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(fields_toolrecord_db))
}


#################################
### 1.2 parser initialization ###
#################################

parser = reqparse.RequestParser()
parser.add_argument('date_time', type=str, required=False, help='date_time required', location=['form', 'args'])
parser.add_argument('date_time_start', type=str, required=False, help='date_time_start required', location=['form', 'args'])
parser.add_argument('date_time_end', type=str, required=False, help='date_time_end required', location=['form', 'args'])
parser.add_argument('colorcode', type=int, required=False, help='colorcode required', location=['form', 'args'])
parser.add_argument('content', type=str, required=False, help='content required', location=['form', 'args'])

####################################
### 2. resource class definition ###
####################################

class ResourceToolRecord(Resource):

    @marshal_with(fields_toolrecord_response)
    # @my_login_required
    def get(self):
        args = parser.parse_args()
        date_time = args.get('date_time')
        item = ToolRecord.query.filter(ToolRecord.date_time == date_time).first()
        response_obj = {
            'status': 200,
            'msg': 'query record success',
            'data': item
        }
        return response_obj

    @marshal_with(fields_toolrecord_response)
    # @my_login_required
    def post(self):
        args = parser.parse_args()
        date_time = args.get('date_time')
        colorcode = args.get('colorcode')
        content = args.get('content')
        item = ToolRecord.query.filter(ToolRecord.date_time == date_time).first()
        item.colorcode = colorcode
        item.content = content
        item.save()
        response_obj = {
            'status': 200,
            'msg': 'update record success',
            'data': item,
        }
        return response_obj
        
    @marshal_with(fields_toolrecord_response)
    # @my_login_required
    def delete(self):
        args = parser.parse_args()
        date_time = args.get('date_time')
        item = ToolRecord.query.filter(ToolRecord.date_time == date_time).first()
        item.delete()
        response_obj = {
            'status': 200,
            'msg': 'delete record success',
            'data': item,
        }
        return response_obj

class ResourceToolRecords(Resource):

    @marshal_with(fields_toolrecords_response)
    # @my_login_required
    def get(self):
        args = parser.parse_args()
        date_time_start = args.get('date_time_start')
        date_time_end = args.get('date_time_end')
        items = ToolRecord.query.filter(and_(ToolRecord.date_time >= date_time_start, ToolRecord.date_time <= date_time_end))
        response_obj = {
            'status': 200,
            'msg': 'query multi records success',
            'data': items
        }
        return response_obj
##############################
### 3. Resourceful Routing ###
##############################

api_db.add_resource(ResourceToolRecord, '/toolrecord/')
api_db.add_resource(ResourceToolRecords, '/toolrecords/')

