"""
FastAPI Application Entry Point.

This module serves as the main entry point for the workout tracking application.
It configures the FastAPI application, sets up CORS middleware, and includes
the necessary routers for authentication and workout functionality.

The application uses SQLAlchemy for database operations and implements
CORS protection for secure communication with the frontend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal

from app.routers import auth, workouts
from app.database import Base, engine


# Initialize FastAPI application
app = FastAPI(
    title="Workout Tracking API",
    description="API for tracking workouts and managing user authentication",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure CORS middleware
# This allows the frontend (running on localhost:3000) to make requests to our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend application URL
    allow_credentials=True,  # Allow cookies in cross-origin requests
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers
)


@app.get("/", response_model=Literal["Health Check Complete"])
async def health_check() -> str:
    """
    Perform a basic health check of the API.

    Returns:
        str: A message indicating the health check is complete
    """
    return "Health Check Complete"


# Include routers for different API endpoints
app.include_router(auth.router)  # Auth routes are already tagged in the router
app.include_router(workouts.router)  # Workout routes are already tagged in the router
