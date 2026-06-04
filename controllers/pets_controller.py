from flask import Blueprint

pets_bp = Blueprint("pets", __name__, url_prefix="/pets")
