from datetime import datetime

from flask import request
from flask_restplus import Resource

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
    def post(self):
        """
        Register a new event
        """
        event = Event(name=request.json.get('name'),
                      location=request.json.get('location'),
                      start_time=datetime.strptime(request.json.get('start_time'), '%Y-%m-%dT%H:%M:%S'),
                      end_time=datetime.strptime(request.json.get('end_time'), '%Y-%m-%dT%H:%M:%S'),
                      email=request.json.get('email'))
        db.session.add(event)
        db.session.commit()
        return event, 201


@ns.route('/<int:event_id>')
@api.response(404, 'Event not found.')
class EventManagement(Resource):

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
        user = self.get(event_id)
        user.delete_flag = 1
        db.session.commit()
        return user, 202


def get_event(name):
    return Event.query.filter(Event.delete_flag==0, Event.name == name).one_or_none()