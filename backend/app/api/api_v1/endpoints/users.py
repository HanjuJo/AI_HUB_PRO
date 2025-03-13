from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[schemas.user.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


import logging
import traceback
from pydantic import ValidationError

logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.user.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
) -> Any:
    """
    Create new user.
    """
    try:
        logger.info(f"Attempting to create user with email: {user_in.email} and username: {user_in.username}")
        
        # 이메일 중복 확인
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            logger.warning(f"User with email {user_in.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system.",
            )
        
        # 사용자 이름 중복 확인
        user = db.query(User).filter(User.username == user_in.username).first()
        if user:
            logger.warning(f"User with username {user_in.username} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this username already exists in the system.",
            )
        
        # 사용자 생성
        logger.info("Creating new user object")
        user = User(
            email=user_in.email,
            username=user_in.username,
            is_superuser=False,  # 일반 회원가입에서는 항상 False
            is_active=True,      # 기본적으로 활성화된 상태로 생성
        )
        
        # 비밀번호 설정
        logger.info("Setting password hash")
        user.set_password(user_in.password)
        
        # DB에 사용자 추가 및 저장
        logger.info("Adding user to database")
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Successfully created user with ID: {user.id}")
        return jsonable_encoder(user.to_dict())
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}",
        )
    except HTTPException as e:
        logger.error(f"HTTP error creating user: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error creating user: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.get("/me", response_model=schemas.user.User)
def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return jsonable_encoder(current_user.to_dict())


@router.put("/me", response_model=schemas.user.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    if user_in.username is not None:
        user = db.query(User).filter(User.username == user_in.username).first()
        if user and user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The username is already taken.",
            )
        current_user.username = user_in.username
    if user_in.email is not None:
        user = db.query(User).filter(User.email == user_in.email).first()
        if user and user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The email is already registered.",
            )
        current_user.email = user_in.email
    if user_in.password is not None:
        current_user.set_password(user_in.password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=schemas.user.User)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.put("/{user_id}", response_model=schemas.user.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.user.UserUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    
    update_data = user_in.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        user.set_password(update_data["password"])
        del update_data["password"]
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
