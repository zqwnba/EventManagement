from flask import jsonify, request

from app.api import api_blueprint
from app.api.events import get_event
from app.api.users import get_user
from app.extensions import db
from app.models.Signup import Signup


@api_blueprint.route('/signups', methods= ['GET'])
def show_user_signups():
    user_email = request.args.get('email')
    if user_email:
        return __jsonify(Signup.query.filter(Signup.user.has(email=user_email)).all()), 200
    else:
        return __jsonify(Signup.query.all()), 200

@api_blueprint.route('/signups/<int:signup_id>', methods= ['GET'])
def show_signup(signup_id):
    return __jsonify(Signup.query.get_or_404(signup_id)), 200

@api_blueprint.route('/signups', methods= ['POST'])
def sign_up():
    user = get_user(request.json.get('user_email'))
    event = get_event(request.json.get('event_name'))
    if user and event:
        signup = Signup.query.filter(Signup.user_id==user.id, Signup.event_id==event.id).all()
        if not signup:
            signup = Signup(user_id=user.id,event_id=event.id)
            db.session.add(signup)
            db.session.commit()
            return __jsonify(signup), 202
        else:
            return jsonify({"message":"user has been signed up to this event."}), 400
    else:
        return jsonify({"message":"user or event is incorrect."}), 400

@api_blueprint.route('/signups', methods= ['DELETE'])
def sign_out():
    user = get_user(request.json.get('user_email'))
    event = get_event(request.json.get('event_name'))
    signup = Signup.query.filter(Signup.user_id==user.id, Signup.event_id==event.id).one_or_none()
    if signup:
        db.session.delete(signup)
        db.session.commit()
        return __jsonify(signup), 202
    else:
        return jsonify({"message":"record is not found."}), 400

def __jsonify(signups):
    if isinstance(signups, list):
        for signup in signups:
            signup.setInfo()
    else:
        signups.setInfo()
    return jsonify(signups)