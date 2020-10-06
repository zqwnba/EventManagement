from datetime import datetime

from flask import request
from flask_restplus import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from app.api.restplus import api
from app.api.serializers import event
from app.extensions import db
from app.models.Event import Event

ns = api.namespace('events', description='Operations related to events')


@ns.route('')
class EventsCollection(Resource):
    @api.marshal_list_with(event)
    def get(self):
        """
        Returns list of events
        """
        return Event.query.filter(Event.delete_flag==0).all(), 200

    @api.response(201, 'Event successfully created.')
    @api.expect(event)
    @api.marshal_with(event)
    def post(self):
        """
        Register a new event
        """
        try:
            event = Event(name=request.json.get('name'),
                      location=request.json.get('location'),
                      start_time=datetime.strptime(request.json.get('start_time'), '%Y-%m-%dT%H:%M:%S'),
                      end_time=datetime.strptime(request.json.get('end_time'), '%Y-%m-%dT%H:%M:%S'),
                      email=request.json.get('email'))
            db.session.add(event)
            db.session.commit()
            return event, 201
        except IntegrityError:
            db.session.rollback()
            raise BadRequest("Event is existing or event name can not be duplicated.")


@ns.route('/<int:event_id>')
@api.response(404, 'Event not found.')
class EventResource(Resource):

    @api.marshal_with(event)
    def get(self, event_id):
        """
        Retrieve a event
        """
        return Event.query.filter(Event.delete_flag==0, Event.id == event_id).first_or_404()

    @api.marshal_with(event)
    def delete(self, event_id):
        """
        Delete a event
        """
        event = Event.query.filter(Event.delete_flag==0, Event.id == event_id).first_or_404()
        event.delete_flag = 1
        db.session.commit()
        return event, 202

    @classmethod
    def get_event(name):
        return Event.query.filter(Event.delete_flag==0, Event.name == name).one_or_none()