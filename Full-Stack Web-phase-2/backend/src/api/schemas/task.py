from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    user_id: int


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    user_id: int
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskToggleComplete(BaseModel):
    completed: bool