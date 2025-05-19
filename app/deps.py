# Dependencies for authentication and database access
# This module provides dependency injection utilities for FastAPI routes,
# including database sessions and JWT-based authentication.

from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from .database import SessionLocal

# Load environment variables from .env file
load_dotenv()

# Authentication configuration
SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

def get_db():
    """
    Provides a database session for each request.

    Creates a new database session using the SessionLocal factory and ensures
    proper cleanup after use through a context manager pattern.

    Yields:
        Session: SQLAlchemy database session object.

    Example:
        @app.get("/users/")
        def get_users(db: db_dependency):
            users = db.query(User).all()
            return users
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Type-annotated dependency for database sessions
db_dependency = Annotated[Session, Depends(get_db)]

# Password hashing configuration using bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 configuration for token-based authentication
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
oauth2_bearer_dependency = Annotated[str, Depends(oauth2_bearer)]

async def get_current_user(token: oauth2_bearer_dependency):
    """
    Validates and decodes JWT token to get current user information.

    This dependency function extracts and validates the user information from
    the JWT token provided in the request header. It ensures that the token
    is valid and contains the required user information.

    Args:
        token (str): JWT token from the request header

    Returns:
        dict: Dictionary containing validated user information (username and id)

    Raises:
        HTTPException: If token is invalid or user information cannot be validated
            - 401 Unauthorized: When token validation fails
            - 401 Unauthorized: When required user information is missing

    Example:
        @app.get("/protected")
        async def protected_route(user: user_dependency):
            return {"message": f"Hello {user['username']}"}
    """
    try:
        # Decode the JWT token using the secret key and specified algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract user information from token payload
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        
        # Validate that required user information is present
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user"
            )
        return {"username": username, "id": user_id}
    except JWTError:
        # Handle JWT validation errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )

# Type-annotated dependency for current user validation
user_dependency = Annotated[dict, Depends(get_current_user)]