"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from celery import Celery
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
celery = Celery()
mail = Mail()
