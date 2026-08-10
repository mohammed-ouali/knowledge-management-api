# Notion-Lite API

An asynchronous RESTful backend API built to support a knowledge management and note-taking platform.

## ERD Diagram

![Entity Relationship Diagram](assets/erd.png)

## Goal of the Project

The objective of this project is to provide a clean, scalable backend service for managing structured notes, organization folders, user comments, and tag categorization. It focuses on applying software engineering practices, async I/O database operations, and clear domain separation.

## Tech Stack

- Framework: FastAPI
- ORM: SQLAlchemy 2.0 (Async)
- Database Driver: Asyncpg / PostgreSQL
- Migration Tool: Alembic
- Data Validation: Pydantic v2

## Architecture

The project adheres to a 3-Layer Clean Architecture:

1. Router Layer (Presentation): Receives incoming HTTP requests, parses parameters, performs validation, and formats HTTP responses.
2. Service Layer (Business Logic): Implements core domain logic, coordinates data operations, and triggers domain exceptions.
3. Repository Layer (Data Access): Handles database operations directly via SQLAlchemy async queries, abstracting storage details from the service layer.

## File Hierarchy

```text
.
├── assets/
│   └── erd.png
├── app/
│   ├── core/
│   │   ├── database.py
│   │   └── exceptions.py
│   ├── models/
│   │   └── ...
│   ├── repositories/
│   │   └── ...
│   ├── routers/
│   │   └── ...
│   ├── schemas/
│   │   └── ...
│   └── services/
│       └── ...
├── alembic/
├── .env
├── alembic.ini
├── main.py
└── requirements.txt
```

## Installation

1. Clone the repository:
```bash
git clone [https://github.com/your-username/notion-lite-api.git](https://github.com/your-username/notion-lite-api.git)
cd notion-lite-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Configure the environment database URL in `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/notes_db
```

5. Apply database migrations:
```bash
alembic upgrade head
```

6. Run the server:
```bash
uvicorn main:app --reload
```