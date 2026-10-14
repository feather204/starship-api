from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")

from app.api import players
from app.api import planets
from app.api import ships