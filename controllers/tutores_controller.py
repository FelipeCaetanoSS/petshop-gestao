from flask import Blueprint

tutores_bp = Blueprint("tutores", __name__, url_prefix="/tutores",
                        template_folder="../templates")
