from flask_restplus import fields
from app.api.restplus import api

event = api.model('Event', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a event'),
    'name': fields.String(required=True, description='Event name'),
    'location': fields.String(required=True, description='Event location'),
    'start_time': fields.DateTime(required=True, description='Event start time'),
    'end_time': fields.DateTime(required=True, description='Event end time'),
    'email': fields.String(required=True, attribute='Event contact'),
})

user = api.model('Event User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
    'email': fields.String(required=True, description='Email address'),
})

signup = api.model('Event sign-up', {
    'user_email': fields.String(required=True, description='User Email address'),
    'event_name': fields.String(required=True, description='Event name'),
})

signup_detail = api.inherit('Event sign-up detail', signup, {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a event sign-up (reservation)'),
    'user_id': fields.Integer(required=True, description='User id'),
    'event_id': fields.Integer(required=True, description='Event id'),
})
