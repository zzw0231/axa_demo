from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserResponse, UserUpdate
from app.utils.logger import logger

router = APIRouter()


# Create a new user (Uses UserCreate schema with email uniqueness check)
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Received request to create user: {user.email}")

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logger.warning(f"User creation failed: Email {user.email} already registered")
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User created successfully: {new_user.email} (ID: {new_user.id})")
    return new_user  # Automatically converts to UserResponse schema


# Get a user by ID (Uses UserResponse schema)
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Searching for user ID: {user_id}")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.error(f"User lookup failed: User ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"User found: {user.email} (ID: {user.id})")
    return user  # Automatically converts to UserResponse schema


# Update a user (Uses UserUpdate schema with duplicate email check)
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    logger.info(f"Received request to update user ID: {user_id}")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"Update failed: User ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent duplicate email update
    if user_update.email and user_update.email != user.email:
        existing_email = db.query(User).filter(User.email == user_update.email).first()
        if existing_email:
            logger.warning(f"Update failed: Email {user_update.email} already in use")
            raise HTTPException(status_code=400, detail="Email already in use")

    if user_update.name:
        user.name = user_update.name
    if user_update.email:
        user.email = user_update.email
    logger.info(f"User updated successfully: {user.email} (ID: {user.id})")
    db.commit()
    db.refresh(user)
    return user  # Automatically converts to UserResponse schema


# Delete a user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to delete user ID: {user_id}")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"Delete failed: User ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    logger.info(f"User deleted successfully: User ID {user_id}")
    return {"message": "User deleted successfully"}
