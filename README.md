# CRUD de ventas: Vue 3 + Axios + Flask

Aplicación con **clientes**, **productos** y **pedidos** (curso Desarrollo Web 036, UMG).
Frontend en Vue 3 + Vue Router + Axios; backend en Flask + Flask-SQLAlchemy + Flask-Migrate; SQLite en desarrollo.

## Requisitos (Windows 10/11)
Python 3.11+, Node.js LTS y Git. Comprobar en PowerShell: `py --version`, `node --version`, `npm --version`.
Si PowerShell bloquea el entorno virtual: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Instalación y ejecución rápida
```powershell
cd crud-vue-flask
.\setup.ps1      # crea .venv, instala dependencias, copia .env y aplica migraciones
.\iniciar.ps1    # abre Flask (5000) y Vite (5173)
```
Abrir http://localhost:5173.

## Ejecución manual
```powershell
# Terminal 1: backend
cd backend
.venv\Scripts\Activate.ps1
flask --app run.py db upgrade
flask --app run.py run --debug

# Terminal 2: frontend
cd frontend
npm install
npm run dev
```

## Pruebas
```powershell
cd backend;  pytest          # 15 pruebas de la API
cd frontend; npm test        # componentes y utilidades
```

## Estructura del proyecto
```
crud-vue-flask/
├── backend/
│   ├── app/
│   │   ├── __init__.py      # fábrica create_app: config, extensiones, blueprint, errores JSON
│   │   ├── extensions.py    # db, migrate, cors (sin app global)
│   │   ├── models.py        # Cliente, Producto, Pedido (tablas y relaciones)
│   │   ├── errors.py        # error() y required() para validar
│   │   └── api/             # blueprint /api: clientes.py, productos.py, pedidos.py
│   ├── migrations/          # historial de Flask-Migrate (Alembic)
│   ├── tests/               # pytest (SQLite en memoria)
│   ├── run.py               # punto de entrada
│   └── requirements.txt / requirements-lock.txt / .env.example
├── frontend/
│   └── src/
│       ├── api/             # http.js (Axios central) + un módulo por recurso
│       ├── components/      # BaseButton, BaseInput, BaseSelect, DataTable, AlertMessage
│       ├── views/           # Dashboard, Clientes, Productos, Pedidos (una por ruta)
│       ├── router/index.js  # rutas con carga perezosa
│       ├── utils/format.js  # moneda y validación de correo
│       └── App.vue, main.js
├── setup.ps1 / iniciar.ps1
```
**Regla:** `components` = piezas reutilizables; `views` = páginas de ruta; `api` = llamadas HTTP; `router` = solo navegación; `models.py` = única definición de tablas.

## Modelo de datos
`clientes 1 ──< pedidos >── 1 productos` (cada pedido lleva un solo producto; un sistema real añadiría `detalle_pedidos`).

## API
| Recurso | Endpoints |
|---|---|
| Clientes | `GET/POST /api/clientes`, `GET/PUT/DELETE /api/clientes/<id>` |
| Productos | `GET/POST /api/productos`, `GET/PUT/DELETE /api/productos/<id>` |
| Pedidos | `GET/POST /api/pedidos`, `GET/PUT/DELETE /api/pedidos/<id>` |
| Salud | `GET /health` |

## Validaciones
- **Backend (autoridad):** campos obligatorios, correo con formato válido y único (409), precio/stock ≥ 0, cantidad entera > 0, stock suficiente, producto activo, estado dentro de `pendiente|pagado|enviado|cancelado`, longitudes máximas.
- **Reglas de integridad:** no se elimina un cliente o producto con pedidos (409); solo se eliminan pedidos cancelados; cancelar un pedido devuelve el stock y reactivarlo lo vuelve a descontar.
- **Frontend:** mismos controles antes de enviar, con mensajes por campo; el interceptor de Axios muestra el mensaje de error de la API.

## Cambios de modelos
```powershell
flask --app run.py db migrate -m "descripcion"
flask --app run.py db upgrade
```

## Seguridad pendiente para producción
Autenticación/autorización, HTTPS, CORS restringido al dominio real, PostgreSQL, servidor WSGI (no el de desarrollo) y `SECRET_KEY` propia.
