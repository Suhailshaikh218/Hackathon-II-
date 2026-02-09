from sqlmodel import Session, select
from .models.task import Task, TaskCreate, TaskUpdate
from .models.user import User
from typing import List, Optional
from datetime import datetime


def create_task(session: Session, task_create: TaskCreate) -> Task:
    """
    Create a new task in the database
    """
    # Convert the TaskCreate to a Task instance
    db_task = Task.model_validate(task_create)
    # Set default values that might not be in the creation request
    # completed field already defaults to False in the model, so we don't override it
    db_task.created_at = datetime.utcnow()
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Retrieve a task by ID for a specific user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def get_tasks_by_user(
    session: Session,
    user_id: int,
    completed: Optional[bool] = None
) -> List[Task]:
    """
    Retrieve all tasks for a specific user, with optional filtering by completion status
    """
    statement = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    statement = statement.order_by(Task.created_at.desc())  # Order by newest first

    tasks = session.exec(statement).all()
    return tasks


def update_task(session: Session, task_id: int, user_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update a task by ID for a specific user
    """
    db_task = get_task_by_id(session, task_id, user_id)
    if not db_task:
        return None

    # Update fields that are provided in the update object
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    """
    Delete a task by ID for a specific user
    """
    db_task = get_task_by_id(session, task_id, user_id)
    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: int, user_id: int, completed: bool) -> Optional[Task]:
    """
    Toggle the completion status of a task
    """
    db_task = get_task_by_id(session, task_id, user_id)
    if not db_task:
        return None

    db_task.completed = completed
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by email
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user