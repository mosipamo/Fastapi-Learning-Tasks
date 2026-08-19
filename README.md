# FastAPI Learning Tasks

A hands-on collection of FastAPI projects, built while working through core FastAPI concepts — from basic routing all the way to a full CRUD application with authentication, a relational database, and Alembic migrations.

Each numbered folder is a self-contained project that builds on the concepts from the one before it.

## Repository structure

```
Fastapi-Learning-Tasks/
├── 01-project/          # Basic routing with an in-memory list
│   ├── books.py
│   └── requirements.txt
├── 02-project/          # Pydantic models, validation, status codes
│   ├── books.py
│   └── requirements.txt
└── 03-project/          # Full app: SQLAlchemy, auth, migrations, tests
    └── TodoApp/
        ├── main.py
        ├── database.py
        ├── models.py
        ├── routers/
        │   ├── auth.py
        │   ├── todos.py
        │   ├── admin.py
        │   └── users.py
        ├── alembic/          # Database migrations
        └── test/             # Pytest test suite
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

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) & [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://docs.pydantic.dev/) for data validation
- [SQLAlchemy](https://www.sqlalchemy.org/) ORM + [Alembic](https://alembic.sqlalchemy.org/) migrations (03-project)
- [PostgreSQL](https://www.postgresql.org/) as the database (03-project)
- [python-jose](https://github.com/mpdavis/python-jose) for JWT encoding/decoding
- [passlib](https://passlib.readthedocs.io/) (bcrypt) for password hashing
- [pytest](https://docs.pytest.org/) for testing

## Getting started

Each project has its own virtual environment and `requirements.txt`, so set them up independently.

### 01-project / 02-project

```bash
cd 01-project        # or 02-project
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
fastapi dev books.py
```

Then open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

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

Then open `http://127.0.0.1:8000/docs`.

### Running tests (03-project)

```bash
cd 03-project/TodoApp
pytest
```
