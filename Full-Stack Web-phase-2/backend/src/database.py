from sqlmodel import create_engine, Session
from typing import Generator
from .config import settings
from sqlmodel import SQLModel
from .models.task import Task  # Import all models here to register them
from .models.user import User  # Import User model to register it


# Create the database engine using the DATABASE_URL from config
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


        
