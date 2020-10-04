from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.configs import MyJSONEncoder
from app.extensions import db
from app import api
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'
# app.config['SECRET_KEY'] = "random string"
#
# db = SQLAlchemy(app)
#
# from app.api.events import events_blueprint
#
# app.register_blueprint(events_blueprint)
#
# if __name__ == '__main__':
#     app.run(debug=True)

#db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = "random string"

    db.init_app(app)
    app.json_encoder = MyJSONEncoder

    app.register_blueprint(api.api_blueprint)

    return app

# import os
#
# from flask import Flask
# #from app.abcdb import sqlite3db
#
# from flask_sqlalchemy import SQLAlchemy
#
# #import sqlite3
# #from flask import g
#
# #DATABASE = 'instance/app.sqlite'
# db = SQLAlchemy()
#
# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         #DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
#     )
#
#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)
#
#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass
#
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#     app.config['SQLALCHEMY_ECHO'] = True
#     db.init_app(app)
#     # with app.app_context():
#     #     db.init_db_command()
#     print("init_app done!")
#     from app.api.events import events_blueprint
#     app.register_blueprint(events_blueprint)
#
#     # def get_db():
#     #     db = getattr(g, '_database', None)
#     #     if db is None:
#     #         db = g._database = sqlite3.connect(DATABASE)
#     #     return db
#     #
#     # @app.teardown_appcontext
#     # def close_connection(exception):
#     #     db = getattr(g, '_database', None)
#     #     if db is not None:
#     #         db.close()
#     #
#     # @app.route('/')
#     # def index():
#     #     cur = get_db().execute("select * from event where id = ?", [0])
#     #     rv = cur.fetchall()
#     #     cur.close()
#     #     return rv[0][1]s
#
#     return app
