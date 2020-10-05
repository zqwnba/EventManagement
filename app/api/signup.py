from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from app.api.events import get_event
from app.api.restplus import api
from app.api.serializers import signup, signup_detail
from app.api.users import get_user
from app.extensions import db
from app.models.Signup import Signup
from app.tasks.email import send_async_email

ns = api.namespace('signups', description='Operations related to events')


@ns.route('')
class SignupsCollection(Resource):

    @api.marshal_list_with(signup_detail)
    def get(self):
        """
        Returns event list of a specific user
        """
        user_email = request.args.get('email')
        if user_email:
            return self.setInfo(Signup.query.filter(Signup.user.has(email=user_email)).all()), 200
        else:
            return self.setInfo(Signup.query.all()), 200


    @api.response(201, 'Sign up successfully.')
    @api.expect(signup)
    @api.marshal_with(signup_detail)
    def post(self):
        """
        Register to a event
        """
        user = get_user(request.json.get('user_email'))
        event = get_event(request.json.get('event_name'))
        if user and event:
            signup = Signup.query.filter(Signup.user_id==user.id, Signup.event_id==event.id).all()
            if not signup:
                signup = Signup(user_id=user.id,event_id=event.id)
                db.session.add(signup)
                db.session.commit()
                self.__send_notification(user, event, signup.id)
                self.__send_invitation(user, event, signup.id)
                return self.setInfo(signup), 201
            else:
                raise BadRequest("user has been signed up to this event.")
        else:
            raise BadRequest("user or event is incorrect.")


    @api.response(202, 'Sign out successfully.')
    @api.expect(signup)
    @api.marshal_with(signup_detail)
    def delete(self):
        """
        Sign out for an event
        """
        user = get_user(request.json.get('user_email'))
        event = get_event(request.json.get('event_name'))
        signup = Signup.query.filter(Signup.user_id==user.id, Signup.event_id==event.id).one_or_none()
        if signup:
            db.session.delete(signup)
            db.session.commit()
            return self.setInfo(signup), 202
        else:
            raise BadRequest("record is not found.")

    @classmethod
    def setInfo(self, signups):
        if isinstance(signups, list):
            for signup in signups:
                signup.setInfo()
        else:
            signups.setInfo()
        return signups


    def __send_notification(self, user, event, signup_id):
        email_data = {
            'subject': 'new sign-up',
            'to': event.email,
            'body': {"signup_id":signup_id, "user":user.email, "event":event.name}
        }
        send_async_email.delay(email_data)


    def __send_invitation(self, user, event, signup_id):
        email_data = {
            'subject': 'invitation',
            'to': user.email,
            'body': {"signup_id":signup_id,
                     "user":user.email,
                     "event":{
                         "name":event.name,
                         "location":event.location,
                         "start_time":event.start_time,
                         "end_time":event.end_time
                     }
                     }
        }
        send_async_email.delay(email_data)


@ns.route('/<int:signup_id>')
class SignupManagement(Resource):

    @api.response(404, 'Not found.')
    @api.marshal_with(signup_detail)
    def get(self, signup_id):
        """
        Retrieve a signup
        """
        return SignupsCollection.setInfo(Signup.query.get_or_404(signup_id)), 200

    @api.marshal_with(signup_detail)
    def delete(self, signup_id):
        """
        Sign out for an event
        """
        signup = self.get(signup_id)
        if signup:
            db.session.delete(signup)
            db.session.commit()
            return SignupsCollection.setInfo(signup), 202
        else:
            raise BadRequest("record is not found.")