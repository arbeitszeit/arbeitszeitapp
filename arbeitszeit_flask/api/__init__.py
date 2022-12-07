from flask import Blueprint
from flask_restx import Api

from .plans import namespace as plans_ns

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api_extension = Api(
    blueprint,
    title="Arbeitszeitapp API",
    version="1.0",
    description="The JSON API of Arbeitszeitapp.",
    doc="/doc/",
)

api_extension.add_namespace(plans_ns)