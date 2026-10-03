def _datos(client, stock=5):
    c = client.post(
        "/api/clientes", json={"nombre": "Ana", "correo": "ana@example.com"}
    ).json
    p = client.post(
        "/api/productos", json={"nombre": "Mouse", "precio": 100, "stock": stock}
    ).json
    return c, p


def test_crear_pedido_descuenta_stock(client):
    c, p = _datos(client)
    r = client.post(
        "/api/pedidos",
        json={"cliente_id": c["id"], "producto_id": p["id"], "cantidad": 2},
    )
    assert r.status_code == 201
    assert r.json["total"] == 200
    assert client.get(f"/api/productos/{p['id']}").json["stock"] == 3


def test_pedido_stock_insuficiente(client):
    c, p = _datos(client, stock=1)
    r = client.post(
        "/api/pedidos",
        json={"cliente_id": c["id"], "producto_id": p["id"], "cantidad": 3},
    )
    assert r.status_code == 409


def test_pedido_cantidad_invalida(client):
    c, p = _datos(client)
    r = client.post(
        "/api/pedidos",
        json={"cliente_id": c["id"], "producto_id": p["id"], "cantidad": 0},
    )
    assert r.status_code == 400


def test_cancelar_devuelve_stock_y_permite_eliminar(client):
    c, p = _datos(client)
    pedido = client.post(
        "/api/pedidos",
        json={"cliente_id": c["id"], "producto_id": p["id"], "cantidad": 2},
    ).json
    assert client.delete(f"/api/pedidos/{pedido['id']}").status_code == 409

    r = client.put(f"/api/pedidos/{pedido['id']}", json={"estado": "cancelado"})
    assert r.status_code == 200
    assert client.get(f"/api/productos/{p['id']}").json["stock"] == 5

    assert client.delete(f"/api/pedidos/{pedido['id']}").status_code == 204


def test_estado_invalido(client):
    c, p = _datos(client)
    pedido = client.post(
        "/api/pedidos",
        json={"cliente_id": c["id"], "producto_id": p["id"], "cantidad": 1},
    ).json
    r = client.put(f"/api/pedidos/{pedido['id']}", json={"estado": "volando"})
    assert r.status_code == 400


def test_no_eliminar_cliente_con_pedidos(client):
    c, p = _datos(client)
    client.post(
        "/api/pedidos",
        json={"cliente_id": c["id"], "producto_id": p["id"], "cantidad": 1},
    )
    assert client.delete(f"/api/clientes/{c['id']}").status_code == 409
    assert client.delete(f"/api/productos/{p['id']}").status_code == 409
