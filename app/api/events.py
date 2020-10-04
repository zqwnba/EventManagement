from datetime import datetime

from flask import jsonify, request
from app.extensions import db

from app.api import api_blueprint
from app.models.Event import Event


@api_blueprint.route('/events', methods= ['GET'])
def show_all_events():
    return jsonify(Event.query.filter(Event.delete_flag==0).all()), 200

@api_blueprint.route('/events/<int:event_id>', methods= ['GET'])
def show_event(event_id):
    return jsonify(Event.query.filter(Event.delete_flag==0, Event.id == event_id).first_or_404()), 200

@api_blueprint.route('/events', methods= ['POST'])
def add_event():
    event = Event(name=request.json.get('name'),
                location=request.json.get('location'),
                start_time=datetime.strptime(request.json.get('start_time'), '%Y-%m-%dT%H:%M:%S'),
                end_time=datetime.strptime(request.json.get('end_time'), '%Y-%m-%dT%H:%M:%S'),
                email=request.json.get('email'))
    db.session.add(event)
    db.session.commit()
    return jsonify(event), 202

@api_blueprint.route('/events/<int:event_id>', methods= ['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    event.delete_flag = 1
    db.session.commit()
    return jsonify(event), 202

def get_event(name):
    return Event.query.filter(Event.delete_flag==0, Event.name == name).one_or_none()