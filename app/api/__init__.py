from flask import Blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

from . import events
from . import users
from . import signup