"""
Workout router module.

This module provides API endpoints for managing workout data, including creating,
retrieving, updating, and deleting workouts. All endpoints require authentication
and are associated with the currently authenticated user.
"""

from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status

from app.models import Workout
from app.deps import db_dependency, user_dependency

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
)

class WorkoutBase(BaseModel):
    """
    Base model for workout data.

    This model defines the common structure for workout data used in requests
    and responses. It includes essential fields for describing a workout.

    Attributes:
        name (str): Name of the workout
        description (Optional[str]): Detailed description of the workout
        duration (int): Duration of the workout in minutes
        date (str): Date of the workout in YYYY-MM-DD format
    """
    name: str
    description: Optional[str] = None
    duration: int
    date: str

class WorkoutCreate(WorkoutBase):
    """
    Model for creating a new workout.

    Extends the WorkoutBase model for workout creation requests. The user_id
    is handled automatically from the authenticated user's token.
    """
    pass

class WorkoutResponse(WorkoutBase):
    """
    Model for workout responses.

    Extends the WorkoutBase model and includes additional fields that are
    present in responses but not in creation requests.

    Attributes:
        id (int): Unique identifier for the workout
        user_id (int): ID of the user who created the workout
    """
    id: int
    user_id: int

    class Config:
        """Pydantic configuration for the response model."""
        from_attributes = True


@router.get("/{workout_id}", response_model=WorkoutResponse)
async def get_workout(
    workout_id: int,
    db: db_dependency,
    user: user_dependency,
):
    """
    Retrieve a specific workout by ID.

    This endpoint fetches a specific workout by its ID. The workout must belong
    to the authenticated user.

    Args:
        workout_id (int): The ID of the workout to retrieve
        db (Session): Database session dependency
        user (dict): Current authenticated user information

    Returns:
        WorkoutResponse: The requested workout details

    Raises:
        HTTPException: 404 if workout not found or doesn't belong to user
    """
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == user["id"]
    ).first()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    return workout


@router.get("/", response_model=List[WorkoutResponse])
async def get_workouts(
    db: db_dependency,
    user: user_dependency
):
    """
    Retrieve all workouts for the authenticated user.

    This endpoint fetches all workouts associated with the currently
    authenticated user.

    Args:
        db (Session): Database session dependency
        user (dict): Current authenticated user information

    Returns:
        List[WorkoutResponse]: List of workouts belonging to the user
    """
    return db.query(Workout).filter(Workout.user_id == user["id"]).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WorkoutResponse)
async def create_workout(
    workout: WorkoutCreate,
    db: db_dependency,
    user: user_dependency,
):
    """
    Create a new workout.

    This endpoint creates a new workout for the authenticated user. The user_id
    is automatically set from the authenticated user's token.

    Args:
        workout (WorkoutCreate): The workout data to create
        db (Session): Database session dependency
        user (dict): Current authenticated user information

    Returns:
        WorkoutResponse: The created workout details
    """
    db_workout = Workout(**workout.model_dump(), user_id=user["id"])
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    workout_id: int,
    db: db_dependency,
    user: user_dependency,
):
    """
    Delete a specific workout.

    This endpoint deletes a workout by its ID. The workout must belong to
    the authenticated user.

    Args:
        workout_id (int): The ID of the workout to delete
        db (Session): Database session dependency
        user (dict): Current authenticated user information

    Raises:
        HTTPException: 404 if workout not found or doesn't belong to user
    """
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == user["id"]
    ).first()
    
    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    db.delete(workout)
    db.commit()

