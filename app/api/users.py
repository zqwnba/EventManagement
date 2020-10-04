from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from app.api import api_blueprint
from app.extensions import db
from app.models.User import User


@api_blueprint.route('/users', methods= ['GET'])
def show_all_users():
    return jsonify(User.query.filter(User.delete_flag==0).all()), 200

@api_blueprint.route('/users/<int:user_id>', methods= ['GET'])
def show_user(user_id):
    return jsonify(User.query.filter(User.delete_flag==0, User.id == user_id).first_or_404()), 200

@api_blueprint.route('/users', methods= ['POST'])
def add_user():
    try:
        user = User(email=request.json.get('email'))
        db.session.add(user)
        db.session.commit()
        return jsonify(user), 202
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message":"email is existing."}), 400

@api_blueprint.route('/users/<int:user_id>', methods= ['DELETE'])
def delete_user(user_id):
    event = User.query.get_or_404(user_id)
    event.delete_flag = 1
    db.session.commit()
    return jsonify(event), 202

def get_user(email):
    return User.query.filter(User.delete_flag==0, User.email == email).one_or_none()