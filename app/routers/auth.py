from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt 
from dotenv import load_dotenv
import os
from ..models import User
from ..deps import db_dependency, bcrypt_context

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],  # Tags for grouping routes in the OpenAPI documentation
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


def authenticate_user(username: str, password: str, db: db_dependency) -> User | bool:
    """
    Authenticates a user by username and password.

    This function checks if a user with the given username exists in the
    database and verifies the password. Returns the user object if authentication
    is successful, False otherwise.

    Args:
        username (str): The username to authenticate
        password (str): The password to verify
        db (Session): SQLAlchemy database session object

    Returns:
        Union[User, bool]: The authenticated user object if successful, False otherwise
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token.

    This function generates a JWT access token for the given username and
    user ID. It includes an expiration time for the token, which can be
    specified as a timedelta object.

    Args:
        username (str): The username for which to create the token
        user_id (int): The ID of the user
        expires_delta (Optional[timedelta]): The expiration time for the token

    Returns:
        str: The generated JWT access token
    """
    to_encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
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
        db (Session): SQLAlchemy database session object
        create_user_request (UserCreateRequest): Request model for creating a new user

    Returns:
        User: The created user object

    Raises:
        HTTPException: If the username already exists in the database
    """
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_model


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    """
    Generates a JWT token for user authentication.

    This endpoint authenticates a user using their username and password,
    and if successful, returns a JWT token that can be used for subsequent
    authenticated requests.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password
        db (Session): SQLAlchemy database session object

    Returns:
        Token: The JWT token response model

    Raises:
        HTTPException: If authentication fails
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

