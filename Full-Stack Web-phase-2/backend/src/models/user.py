from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    email: str
    password: str


class UserRegister(UserBase):
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None


class UserAuth(UserRead):
    hashed_password: str