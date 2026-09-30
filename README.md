# FastAPI Learning Tasks

A hands-on collection of FastAPI projects, built while working through core FastAPI concepts — from basic routing all the way to a full CRUD application with authentication, a relational database, and Alembic migrations.

The repo has two tracks:

- **Core track** (`01-project` → `03-project`): a progressive path that ends in a complete, database-backed app.
- **Concept drills** (named folders): small, single-topic projects, each focused on one FastAPI feature.

Every folder is self-contained with its own code and tests.

## Repository structure

```
Fastapi-Learning-Tasks/
├── 01-project/                    # Basic routing with an in-memory list
├── 02-project/                    # Pydantic models, validation, status codes
├── 03-project/                    # Full app: SQLAlchemy, auth, migrations, tests
│   └── TodoApp/
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── routers/               # auth, todos, admin, users
│       ├── alembic/               # Database migrations
│       └── test/                  # Pytest test suite
│
├── salam-quera/                   # Hello-world routing & response builders
├── signup-namava/                 # Pydantic request models (signup/login)
├── validated-product-divar/       # Field constraints & validators
├── error-handling-filimo/         # Custom exception handlers
├── custom-response-tapsi/         # Status codes, headers, cookies
├── masir-karbar-digikala/         # Nested path parameters
├── jostojuye-mahsul-snapp/        # Query params: search & filter
├── pagination-dependency-digikala/# Reusable pagination dependency
├── resource-dependency-snappfood/ # yield dependencies & app-wide guards
├── async-aggregator-divar/        # async/await, gather, timeouts
└── modular-api-snapp/             # APIRouter & package layout
```

## Projects

### 01-project — Books API (basics)
A first pass at FastAPI routing using a plain Python list as the data store. Covers:
- Path parameters and query parameters
- `GET`, `POST`, `PUT`, and `DELETE` endpoints
- Reading the request body with `Body()`

### 02-project — Books API (validation & structure)
Builds on 01-project by introducing proper data modeling and validation. Covers:
- Pydantic models (`BaseModel`, `Field`) for request validation
- Optional fields and custom validation rules (length, ranges)
- `Path()` and `Query()` constraints
- Explicit HTTP status codes and `HTTPException` error handling
- Example schemas via `json_schema_extra` (visible in the auto-generated docs)

### 03-project — TodoApp (full application)
A complete, database-backed Todo application. Covers:
- **SQLAlchemy** models and a Postgres-backed database (`database.py`, `models.py`)
- **Alembic** for schema migrations
- **Authentication** with OAuth2 password flow, JWT access tokens, and bcrypt password hashing (`routers/auth.py`)
- **Role-based access** for admin-only operations (`routers/admin.py`)
- Full CRUD for todos scoped to the logged-in user (`routers/todos.py`)
- User profile management, including password and phone number updates (`routers/users.py`)
- A `pytest` test suite covering auth, todos, admin, and users

#### API overview

| Router | Prefix | Endpoints |
|---|---|---|
| Auth | `/auth` | `POST /` (register), `POST /token` (login, returns JWT) |
| Todos | `/todos` | `GET /`, `GET /todo/{todo_id}`, `POST /todo`, `PUT /todo/{todo_id}`, `DELETE /todo/{todo_id}` |
| Admin | `/admin` | `GET /todos`, `DELETE /todo/{todo_id}` |
| Users | `/users` | `GET /`, `PUT /password`, `PUT /change_phone_number/{phone_number}` |

Plus a top-level `GET /healthy` check.

---

## Concept drills

Each drill is a tiny service around a real-world-shaped domain (Quera, Divar, Tapsi, Snapp, Digikala…), so the same concept gets practised in context.

### salam-quera — Routing & response builders
The simplest project: a greeting/status service split across `main.py`, `responses.py` (payload builders), and `data.py` (static data).
- `def` handlers with return type hints; response construction kept out of the route
- Endpoints: `GET /`, `/health`, `/info`, `/ping`, `/team`, `/services`, `/stats`

### signup-namava — Pydantic request models
In-memory account signup/login service.
- `SignupRequest` / `LoginRequest` models, `model_dump()`, optional fields with defaults
- Response shaping so the `password` field is never echoed back
- Endpoints: `GET /`, `POST /signup`, `GET /accounts?prefix=&limit=`, `GET /accounts/{username}`, `POST /login`

### validated-product-divar — Constraints & validators
Divar-style classified listings with strict input validation.
- `Field` constraints (`min_length`, `gt`, `le`) and `@field_validator` (category whitelist, title trimming)
- Separate `response_model` input/output schemas so `seller_phone` is never exposed
- Endpoints: `GET /`, `POST /products`, `GET /products/{product_id}`

> Note: this folder contains a stray nested copy of `signup-namava/` (identical files); it is not part of the project.

### error-handling-filimo — Exception handling
Movie playback with subscription tier, age, and region restrictions.
- Custom exception class + `@app.exception_handler`, structured `{"error": {"code", "message"}}` bodies
- `HTTPException` (404/403/409), a `JSONResponse` with a custom `X-Error-Code` header, and 451 for region locks
- Endpoints: `GET /`, `GET /movies/{movie_id}`, `GET /movies/{movie_id}/play?user_id=`, `GET /movies/{movie_id}/availability?region=`, `POST /subscriptions`

### custom-response-tapsi — Status codes, headers & cookies
Ride-hailing lifecycle: requested → ongoing → completed.
- Non-default status codes (`201`, `204`), mutating the injected `Response` for `Location`, `X-Ride-Id`, `X-Total-Count`
- `response.set_cookie()`, manual validation raising `HTTPException(422)`, `409` on invalid state transitions
- Endpoints: `GET /`, `POST /rides`, `GET /rides`, `GET /rides/{ride_id}`, `PATCH /rides/{ride_id}/status`, `DELETE /rides/{ride_id}`, `GET /session`

### masir-karbar-digikala — Nested path parameters
Internal panel with user → order hierarchy and computed summaries.
- Multi-level path params (`/users/{user_id}/orders/{order_id}`), helpers kept in `helpers.py`, 422 on non-integer ids
- Endpoints: `GET /`, `/users`, `/users/{user_id}`, `/users/{user_id}/orders`, `/users/{user_id}/orders/{order_id}`, `/users/{user_id}/summary`

### jostojuye-mahsul-snapp — Query params, search & filtering
Snapp Market product search over 22 groceries.
- Query params with defaults (`q`, `category`, `page`, `page_size`), case-insensitive substring match, exact category filter
- Offset slicing returning `{total, page, page_size, items}`
- Endpoints: `GET /`, `GET /products`

### pagination-dependency-digikala — Reusable pagination dependency
Product and order listings sharing one sort/pagination dependency.
- `paginate()` in `deps.py`, pre-configured per resource with `functools.partial`, `Annotated` aliases (`ProductPagination`, `OrderPagination`)
- Validation of `order`/`sort` → 422, page/size clamping (max 50)
- Endpoints: `GET /`, `GET /products?min_price=`, `GET /orders?min_total=`

### resource-dependency-snappfood — `yield` dependencies & app-wide guards
Restaurant menu API protected by an API key and backed by a connection resource.
- Dependency with `yield` for resource teardown, `dependencies=[Depends(require_api_key)]` applied app-wide, header dependency (`X-Api-Key` → 401), `Annotated[..., Depends(...)]`
- Endpoints: `GET /`, `GET /menu?page=&size=`, `GET /menu/{item_id}`

### async-aggregator-divar — Async handlers & fan-out
Post-detail aggregator that fans out to 5–7 simulated microservices and merges the results.
- `async def` handlers, `asyncio.gather(..., return_exceptions=True)`, `asyncio.wait_for` timeouts with graceful degradation (`degraded: [...]`)
- Optional sections via a validated query param; nested fan-out in `/batch`
- Endpoints: `GET /`, `GET /aggregate/{post_token}?sections=...`, `GET /batch?tokens=...`
- The test suite asserts a full aggregate finishes in < 0.6s, proving requests run concurrently

### modular-api-snapp — APIRouter & package layout
Users/rides API split into a proper Python package.
- `app/` package with `__init__.py`, `APIRouter` with `prefix`/`tags`, `app.include_router(...)`, optional query filters
- Run with `app.main:app`
- Endpoints: `GET /`, `/users?role=`, `/users/{user_id}`, `/rides?status=`, `/rides/{ride_id}`

---

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) & [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://docs.pydantic.dev/) for data validation
- [SQLAlchemy](https://www.sqlalchemy.org/) ORM + [Alembic](https://alembic.sqlalchemy.org/) migrations (03-project)
- [PostgreSQL](https://www.postgresql.org/) as the database (03-project)
- [python-jose](https://github.com/mpdavis/python-jose) for JWT encoding/decoding
- [passlib](https://passlib.readthedocs.io/) (bcrypt) for password hashing
- [pytest](https://docs.pytest.org/) / `unittest` + [httpx](https://www.python-httpx.org/) (`TestClient`) for testing

## Getting started

Each project has its own virtual environment, so set them up independently.

```bash
cd <project-folder>
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt   # if present, otherwise: pip install fastapi uvicorn
```

### 01-project / 02-project

```bash
fastapi dev books.py
```

### 03-project (TodoApp)

The `requirements.txt` here only lists `fastapi` and `uvicorn`; you'll also need the packages the app imports for the database, auth, and migrations:

```bash
cd 03-project
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart pytest
```

Before running the app:

1. **Database** — `TodoApp/database.py` currently points at a local PostgreSQL instance with a hardcoded connection string. Update it (ideally by loading it from an environment variable) to match your own Postgres setup, or switch it back to the commented-out SQLite line for a zero-config local run.
2. **Migrations** — apply the Alembic migrations to create/update the schema:
   ```bash
   cd TodoApp
   alembic upgrade head
   ```
3. **Run the app**:
   ```bash
   fastapi dev main.py
   ```
   or
   ```bash
   uvicorn main:app --reload
   ```

### Concept drills

```bash
cd <drill-folder>
fastapi dev main.py           # modular-api-snapp: uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

> Only `01-project`, `02-project`, and `salam-quera` ship a `requirements.txt`; the other drills use a minimal dependency set (`fastapi`, `uvicorn`, `httpx` for tests).

## Running tests

```bash
# 03-project
cd 03-project/TodoApp
pytest

# Any concept drill
cd <drill-folder>
python -m unittest discover -s test      # or: pytest
```

All drills ship a `test/test_sample.py` built on `unittest.TestCase` + `fastapi.testclient.TestClient`.
