from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt 
from dotenv import load_dotenv
import os
from api.models import User
from api.deps import db_dependency, ybcrypt_context

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["auth"], # Tags for grouping routes in the OpenAPI documentation
)

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

class UserCreateRequest(BaseModel):
    """
    Request model for creating a new user.

    This model defines the structure of the request body for creating a new user.
    It includes the username and password fields, which are required for user
    registration.

    Attributes:
        username (str): Unique username for the new user.
        password (str): Password for the new user.
    """
    username: str
    password: str

class Token(BaseModel):
    """
    Model for JWT token response.

    This model defines the structure of the response body for JWT token generation.
    It includes the access token and its type.

    Attributes:
        access_token (str): The generated JWT access token.
        token_type (str): The type of the token (usually "bearer").
    """
    access_token: str
    token_type: str


    def authenticate_user(username: str, password: str, db: db_dependency):
        """
        Authenticates a user by username.

        This function checks if a user with the given username exists in the
        database and returns the user object if found. If not found, it raises
        an HTTPException with a 404 status code.

        Args:
            db (Session): SQLAlchemy database session object.
            username (str): The username to authenticate.

        Returns:
            User: The authenticated user object.

        Raises:
            HTTPException: If the user is not found in the database.
        """
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False
        if not bycrypt_context.verify(password, user.hashed_password):
            return False
        return user
    
    def create_access_token(username: str, user_id: int, expires_delta: timedelta):
        """
        Creates a JWT access token.

        This function generates a JWT access token for the given username and
        user ID. It includes an expiration time for the token, which can be
        specified as a timedelta object.

        Args:
            username (str): The username for which to create the token.
            user_id (int): The ID of the user.
            expires_delta (timedelta, optional): The expiration time for the token.

        Returns:
            str: The generated JWT access token.
        """
        to_encode = {"sub": username, "id": user_id}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def create_user(db: db_dependency, create_user_request: UserCreateRequest):
        """
        Creates a new user.

        This endpoint allows the creation of a new user in the system. It requires
        a username and password in the request body. If the user is created successfully,
        it returns a 201 status code.

        Args:
            db (Session): SQLAlchemy database session object.
            create_user_request (UserCreateRequest): Request model for creating a new user.

        Returns:
            User: The created user object.

        Raises:
            HTTPException: If the username already exists in the database.
        """
        create_user_model = User(
            username=create_user_request.username,
            hashed_password=bycrypt_context.hash(create_user_request.password)
        )
        
        db.add(create_user_model)
        db.commit()
       
