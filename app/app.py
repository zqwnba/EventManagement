# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from app import api
#
# db = SQLAlchemy()
#
# def create_app(config=None):
#     app = Flask(__name__, instance_relative_config=True)
#
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#     app.config['SQLALCHEMY_ECHO'] = True
#     app.config['SECRET_KEY'] = "random string"
#
#     db.init_app(app)
#
#     app.register_blueprint(api.events.events_blueprint)
#
#     return app