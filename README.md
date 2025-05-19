# FastAPI UV Test Project

A FastAPI backend application using UV package manager, designed to work with a Next.js frontend.

## Project Overview

This project demonstrates:

- FastAPI setup with UV package manager
- CORS configuration for Next.js integration
- SQLAlchemy database models
- JWT-based authentication
- Environment variable management

## Project Structure

```
.
├── app/                    # Main application directory
│   ├── __init__.py        # Python package indicator
│   ├── database.py        # Database configuration
│   ├── deps.py            # Dependency injection utilities
│   ├── main.py            # FastAPI application entry point
│   └── models.py          # SQLAlchemy models
├── .env                    # Environment variables (not in version control)
├── .gitignore             # Git ignore rules
├── pyproject.toml         # Project dependencies and metadata
└── requirements.txt       # Python dependencies
```

## Setup Guide

### 1. Initial Setup

1. Create a new directory and initialize the project:

```bash
mkdir fastapi_uv_test
cd fastapi_uv_test
```

2. Install UV package manager (if not already installed):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
```

### 2. Install Dependencies

Install required packages using UV:

```bash
uv pip install fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] passlib[bcrypt] python-multipart python-dotenv
```

### 3. Configure CORS Middleware

Set up CORS in `app/main.py` to allow requests from Next.js frontend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Database Configuration

1. Create `app/database.py` for SQLAlchemy setup:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

2. Define models in `app/models.py`:

- User model with authentication fields
- Additional models for your application
- SQLAlchemy relationships

### 5. Authentication Setup

1. Generate a secure secret key:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

2. Create `.env` file:

```env
AUTH_SECRET_KEY=your_generated_secret_key
AUTH_ALGORITHM=HS256
API_URL=http://localhost:3000
```

3. Set up authentication dependencies in `app/deps.py`:

- Database session management
- Password hashing with bcrypt
- JWT token validation
- User authentication utilities

### .6 Going Ahead to Create WorkOuts

### . Security Best Practices

1. Add `.env` to `.gitignore`:

```gitignore
.env
.env.*
```

2. Store different secret keys for different environments
3. Implement proper error handling
4. Use secure password hashing

## Development Server

Run the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

Required environment variables:

- `AUTH_SECRET_KEY`: JWT secret key (generate using provided command)
- `AUTH_ALGORITHM`: JWT algorithm (default: HS256)
- `API_URL`: Frontend application URL
