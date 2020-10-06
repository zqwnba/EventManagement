from flask import request
from flask_restplus import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

from app.api.restplus import api
from app.api.serializers import user
from app.extensions import db
from app.models.User import User

ns = api.namespace('users', description='Operations related to users')


@ns.route('')
class UsersCollection(Resource):
    @api.marshal_list_with(user)
    def get(self):
        """
        Returns list of users
        """
        return User.query.filter(User.delete_flag==0).all(), 200

    @api.response(201, 'User successfully created.')
    @api.expect(user)
    def post(self):
        """
        Register a new user
        """
        try:
            user = User(email=request.json.get('email'))
            db.session.add(user)
            db.session.commit()
            return None, 201
        except IntegrityError:
            db.session.rollback()
            raise BadRequest("email is existing.")


@ns.route('/<int:user_id>')
@api.response(404, 'User not found.')
class UserAccount(Resource):

    @api.marshal_with(user)
    def get(self, user_id):
        """
        Retrieve a user
        """
        return User.query.filter(User.delete_flag==0, User.id == user_id).first_or_404()

    @api.marshal_with(user)
    def delete(self, user_id):
        """
        Delete a user
        """
        user = User.query.filter(User.delete_flag==0, User.id == user_id).first_or_404()
        user.delete_flag = 1
        db.session.commit()
        return user, 202

    @classmethod
    def get_user(cls, email):
        return User.query.filter(User.delete_flag==0, User.email == email).one_or_none()