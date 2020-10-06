import os

from flask import Flask, Blueprint

from app.api.restplus import api
from app.extensions import db, mail, celery
from app.api.users import ns as users_namespace
from app.api.events import ns as events_namespace
from app.api.signup import ns as signups_namespace

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    # SQLALCHEMY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    # Celery configuration
    app.config['CELERY_BROKER_URL'] = "sqla+sqlite:///instance/app.sqlite"
    app.config['RESULT_BACKEND'] = "db+sqlite:///instance/app.sqlite"
    # Flask-Mail configuration
    # app.config['MAIL_SERVER'] = 'smtp.events.com'
    # app.config['MAIL_PORT'] = 587
    # app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = 'contact@events.com'

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_celery(app)
    db.init_app(app)
    mail.init_app(app)

    api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    api.init_app(api_blueprint)
    api.add_namespace(users_namespace)
    api.add_namespace(events_namespace)
    api.add_namespace(signups_namespace)
    app.register_blueprint(api_blueprint)

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
