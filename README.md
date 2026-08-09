# Notes App API

An asynchronous RESTful API for managing users, folders, notes, comments, and tags. Built with FastAPI, SQLAlchemy (AsyncIO), PostgreSQL, and Pydantic following a Clean 3-Layer Architecture.

---

## 🏗 Architecture

The project follows a modular, three-layer architectural pattern to maintain clear separation of concerns:

1. **Router Layer (`app/routers`)**: Handles HTTP requests, path/query parameters, and response serialization.
2. **Service Layer (`app/services`)**: Enforces core domain business logic and raises domain exceptions.
3. **Repository Layer (`app/repositories`)**: Encapsulates database interactions using SQLAlchemy async sessions.

---

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLAlchemy 2.0 (Async)](https://www.sqlalchemy.org/)
- **Database**: PostgreSQL
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)

---

## 📁 Project Structure

```text
app/
├── core/               # App configuration, database setup, domain exceptions
├── models/             # SQLAlchemy ORM models & table relationships
├── schemas/            # Pydantic schemas for request/response validation
├── repositories/       # Async database access layer
├── services/           # Business logic layer
└── routers/            # FastAPI API route definitions
main.py                 # Application entrypoint & middleware configuration