from flask import Blueprint

ads_bp = Blueprint('ads', __name__, url_prefix='/ads')
from . import routes
