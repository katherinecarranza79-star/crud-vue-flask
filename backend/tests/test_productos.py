def test_crud_producto(client):
    r = client.post(
        "/api/productos", json={"nombre": "Teclado", "precio": 150.5, "stock": 10}
    )
    assert r.status_code == 201
    pid = r.json["id"]
    assert r.json["precio"] == 150.5

    r = client.put(
        f"/api/productos/{pid}",
        json={"nombre": "Teclado mecánico", "precio": 200, "stock": 5, "activo": False},
    )
    assert r.status_code == 200
    assert r.json["activo"] is False

    assert client.delete(f"/api/productos/{pid}").status_code == 204


def test_producto_valores_negativos(client):
    r = client.post("/api/productos", json={"nombre": "X", "precio": -1, "stock": 1})
    assert r.status_code == 400


def test_producto_precio_invalido(client):
    r = client.post("/api/productos", json={"nombre": "X", "precio": "abc", "stock": 1})
    assert r.status_code == 400


def test_producto_campos_obligatorios(client):
    r = client.post("/api/productos", json={"nombre": "X"})
    assert r.status_code == 400
