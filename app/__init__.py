import os

from flask import Flask

from app.configs import MyJSONEncoder
from app.extensions import db, mail, celery


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

#celery = Celery('tasks', broker="sqla+sqlite:///instance/app.sqlite")


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = "random string"
    # SQLALCHEMY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    # Celery configuration
    app.config['CELERY_BROKER_URL'] = "sqla+sqlite:///instance/app.sqlite"
    app.config['RESULT_BACKEND'] = "db+sqlite:///instance/app.sqlite"
    # Flask-Mail configuration
    # app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = 'contact@events.com'

    #celery.conf.update(app.config)
    init_celery(app)
    db.init_app(app)
    mail.init_app(app)
    app.json_encoder = MyJSONEncoder

    from app import api
    app.register_blueprint(api.api_blueprint)

    return app

def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["RESULT_BACKEND"]
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# @celery.task
# def send_async_emailxx(email_data):
#     with create_app().app_context():
#         msg = Message(email_data['subject'],
#                       recipients=email_data['to'],
#                       body=email_data['body'])
#         mail.send(msg)

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
