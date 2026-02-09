from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from .user import User


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id", description="ID of the user who owns this task")  # Index for performance
    completed: bool = Field(default=False, index=True)  # Index for filtering by completion status
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to user
    user: Optional[User] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    user_id: Optional[int] = Field(default=None, description="ID of the user who owns this task")


class TaskRead(TaskBase):
    id: int
    user_id: int
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskToggleComplete(SQLModel):
    completed: bool