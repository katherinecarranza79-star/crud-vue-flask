def test_crear_y_listar_cliente(client):
    response = client.post(
        "/api/clientes",
        json={"nombre": "Cliente de prueba", "correo": "prueba@example.com"},
    )
    assert response.status_code == 201
    assert response.json["nombre"] == "Cliente de prueba"

    response = client.get("/api/clientes")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_cliente_campos_obligatorios(client):
    response = client.post("/api/clientes", json={"nombre": "Sin correo"})
    assert response.status_code == 400
    assert "correo" in response.json["details"]


def test_cliente_correo_invalido(client):
    response = client.post(
        "/api/clientes", json={"nombre": "Ana", "correo": "no-es-correo"}
    )
    assert response.status_code == 400


def test_cliente_correo_duplicado(client):
    body = {"nombre": "Ana", "correo": "ana@example.com"}
    assert client.post("/api/clientes", json=body).status_code == 201
    assert client.post("/api/clientes", json=body).status_code == 409


def test_actualizar_y_eliminar_cliente(client):
    creado = client.post(
        "/api/clientes", json={"nombre": "Ana", "correo": "ana@example.com"}
    ).json
    r = client.put(
        f"/api/clientes/{creado['id']}",
        json={"nombre": "Ana López", "correo": "ana@example.com", "telefono": None},
    )
    assert r.status_code == 200
    assert r.json["nombre"] == "Ana López"
    assert client.delete(f"/api/clientes/{creado['id']}").status_code == 204
    assert client.get(f"/api/clientes/{creado['id']}").status_code == 404
