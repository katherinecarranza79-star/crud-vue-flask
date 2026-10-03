from datetime import datetime, timezone

from .extensions import db


def _now():
    return datetime.now(timezone.utc)


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(160), unique=True, nullable=False, index=True)
    telefono = db.Column(db.String(30), nullable=True)
    creado_en = db.Column(db.DateTime, default=_now, nullable=False)

    pedidos = db.relationship("Pedido", back_populates="cliente", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "telefono": self.telefono,
        }


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(300), nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    pedidos = db.relationship("Pedido", back_populates="producto", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": float(self.precio),
            "stock": self.stock,
            "activo": self.activo,
        }


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(30), nullable=False, default="pendiente")
    creado_en = db.Column(db.DateTime, default=_now, nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    producto = db.relationship("Producto", back_populates="pedidos")

    def to_dict(self):
        return {
            "id": self.id,
            "cantidad": self.cantidad,
            "estado": self.estado,
            "cliente_id": self.cliente_id,
            "producto_id": self.producto_id,
            "cliente": self.cliente.nombre,
            "producto": self.producto.nombre,
            "total": round(float(self.producto.precio) * self.cantidad, 2),
        }
