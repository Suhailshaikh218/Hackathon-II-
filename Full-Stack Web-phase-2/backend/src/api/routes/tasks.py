from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ...database import get_session
from ...models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskToggleComplete
from ...models.user import User
from ...auth import get_current_active_user
from ...services import (
    create_task,
    get_task_by_id,
    get_tasks_by_user,
    update_task,
    delete_task,
    toggle_task_completion
)

router = APIRouter(prefix="/api", tags=["tasks"])


@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_new_task(
    user_id: int, 
    task: TaskCreate, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task with required title and optional description
    """
    # Ensure the user can only create tasks for themselves
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create tasks for this user")
    
    # Override user_id from the path parameter to ensure consistency
    task.user_id = user_id
    return create_task(session, task)


@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def read_tasks(
    user_id: int, 
    completed: bool = None, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    List all tasks belonging to a given user_id, with optional filtering by completion status
    """
    # Ensure the user can only access their own tasks
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access tasks for this user")
        
    return get_tasks_by_user(session, user_id, completed)


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def read_task(
    user_id: int, 
    task_id: int, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a single task by id for a specific user
    """
    # Ensure the user can only access their own tasks
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access tasks for this user")
        
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_existing_task(
    user_id: int,
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Update task fields (title, description, completion state)
    """
    # Ensure the user can only update their own tasks
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update tasks for this user")
        
    updated_task = update_task(session, task_id, user_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_existing_task(
    user_id: int, 
    task_id: int, 
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task permanently
    """
    # Ensure the user can only delete their own tasks
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete tasks for this user")
        
    success = delete_task(session, task_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_complete(
    user_id: int,
    task_id: int,
    task_toggle: TaskToggleComplete,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion state
    """
    # Ensure the user can only toggle completion for their own tasks
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update tasks for this user")
        
    task = toggle_task_completion(session, task_id, user_id, task_toggle.completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task