from flask import Blueprint

api_bp = Blueprint("api", __name__)

from . import clientes, pedidos, productos  # noqa: E402, F401
