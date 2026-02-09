from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlmodel import Session, select
from typing import Dict
from ... import auth
from ...database import get_session
from ...models.user import UserRegister, UserLogin, UserRead, User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserRead)
def register_user(user_data: UserRegister, session: Session = Depends(get_session)):
    """Register a new user."""
    # Check if user already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = auth.get_password_hash(user_data.password)
    
    # Create new user
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


@router.post("/login")
def login_user(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """Authenticate user and return access token."""
    user = auth.authenticate_user(session, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserRead.from_orm(user) if hasattr(UserRead, 'from_orm') else UserRead(**user.dict())
    }