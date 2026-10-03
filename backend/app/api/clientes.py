import re

from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from ..errors import error, required
from ..extensions import db
from ..models import Cliente
from . import api_bp

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def cliente_data(data):
    missing = required(data, ["nombre", "correo"])
    if missing:
        return None, error("Faltan campos obligatorios", details=missing)

    nombre = str(data["nombre"]).strip()
    correo = str(data["correo"]).strip().lower()
    telefono = str(data.get("telefono") or "").strip()

    if len(nombre) > 120:
        return None, error("El nombre no puede superar 120 caracteres")
    if len(correo) > 160 or not EMAIL_RE.match(correo):
        return None, error("El correo no es válido")
    if len(telefono) > 30:
        return None, error("El teléfono no puede superar 30 caracteres")

    return {"nombre": nombre, "correo": correo, "telefono": telefono}, None


@api_bp.get("/clientes")
def listar_clientes():
    clientes = Cliente.query.order_by(Cliente.id.desc()).all()
    return jsonify([cliente.to_dict() for cliente in clientes])


@api_bp.get("/clientes/<int:cliente_id>")
def obtener_cliente(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    return jsonify(cliente.to_dict())


@api_bp.post("/clientes")
def crear_cliente():
    data, response = cliente_data(request.get_json(silent=True) or {})
    if response:
        return response

    cliente = Cliente(**data)
    db.session.add(cliente)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error("El correo ya está registrado", 409)
    return jsonify(cliente.to_dict()), 201


@api_bp.put("/clientes/<int:cliente_id>")
def actualizar_cliente(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    data, response = cliente_data(request.get_json(silent=True) or {})
    if response:
        return response

    for key, value in data.items():
        setattr(cliente, key, value)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error("El correo ya está registrado", 409)
    return jsonify(cliente.to_dict())


@api_bp.delete("/clientes/<int:cliente_id>")
def eliminar_cliente(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    if cliente.pedidos:
        return error("No se puede eliminar un cliente con pedidos", 409)
    db.session.delete(cliente)
    db.session.commit()
    return "", 204
