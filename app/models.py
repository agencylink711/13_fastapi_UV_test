from sqlalchemy import column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Define the many-to-many association table for workouts and routines
# This table manages the relationship between workouts and routines,
# allowing a workout to be part of multiple routines and vice versa
workout_routine_association = Table(
    "workout_routine", Base.metadata,
    column("workout_id", Integer, ForeignKey("workouts.id")),
    column("routine_id", Integer, ForeignKey("routines.id")),
)


class User(Base):
    """
    User model representing application users.

    This class defines the structure for storing user information in the database.
    Each user can have multiple workouts and routines associated with them.

    Attributes:
        id (int): Primary key for user identification
        username (str): Unique username for the user
        hash_password (str): Hashed version of the user's password for security
        workouts (relationship): One-to-many relationship with Workout model
        routines (relationship): One-to-many relationship with Routine model
    """
    __tablename__ = "users"

    id = column(Integer, primary_key=True, index=True)
    username = column(String, unique=True, index=True)
    hash_password = column(String)

    # Relationship definitions
    workouts = relationship("Workout", back_populates="user")
    routines = relationship("Routine", back_populates="user")


class Workout(Base):
    """
    Workout model representing individual workout sessions.

    This class defines the structure for storing workout information. Each workout
    belongs to a user and can be part of multiple routines through the
    workout_routine_association table.

    Attributes:
        id (int): Primary key for workout identification
        name (str): Name of the workout
        description (str): Detailed description of the workout
        duration (int): Duration of the workout in minutes
        date (str): Date of the workout in YYYY-MM-DD format
        user_id (int): Foreign key linking to the user who created the workout
        user (relationship): Relationship to the User model
        routines (relationship): Many-to-many relationship with Routine model
    """
    __tablename__ = "workouts"

    id = column(Integer, primary_key=True, index=True)
    name = column(String, index=True)
    description = column(String, index=True)
    duration = column(Integer)  # Duration in minutes
    date = column(String)  # Date in YYYY-MM-DD format
    user_id = column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="workouts")
    routines = relationship("Routine", secondary=workout_routine_association, back_populates="workouts")


class Routine(Base):
    """
    Routine model representing workout routines/programs.

    This class defines the structure for storing workout routines. Each routine
    belongs to a user and can contain multiple workouts through the
    workout_routine_association table.

    Attributes:
        id (int): Primary key for routine identification
        name (str): Name of the routine
        description (str): Detailed description of the routine
        duration (int): Total duration of the routine in minutes
        date (str): Creation date of the routine in YYYY-MM-DD format
        user_id (int): Foreign key linking to the user who created the routine
        user (relationship): Relationship to the User model
        workouts (relationship): Many-to-many relationship with Workout model
    """
    __tablename__ = "routines"

    id = column(Integer, primary_key=True, index=True)
    name = column(String, index=True)
    description = column(String, index=True)
    duration = column(Integer)  # Duration in minutes
    date = column(String)  # Date in YYYY-MM-DD format
    user_id = column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="routines")
    workouts = relationship("Workout", secondary=workout_routine_association, back_populates="routines")

# Establish the bidirectional relationship between Workout and Routine
Workout.routines = relationship("Routine", secondary=workout_routine_association, back_populates="workouts")