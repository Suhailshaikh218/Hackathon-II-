import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from main import app
from src.database import get_session
from src.models.task import Task


# Create an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    from src.models.task import Task
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    from src.database import get_session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_task(client: TestClient):
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "user_id": 1
    }
    
    response = client.post("/api/tasks/", json=task_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["user_id"] == 1
    assert data["completed"] is False
    assert "id" in data


def test_get_task_by_id(client: TestClient, session: Session):
    """Test retrieving a single task by ID"""
    # First create a task
    task_data = {
        "title": "Get Test Task",
        "description": "Task for get test",
        "user_id": 1
    }
    
    create_response = client.post("/api/tasks/", json=task_data)
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Then retrieve it
    response = client.get(f"/api/tasks/{task_id}?user_id=1")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Test Task"


def test_get_tasks_by_user(client: TestClient, session: Session):
    """Test retrieving all tasks for a user"""
    # Create multiple tasks for the same user
    task_data_1 = {
        "title": "First Task",
        "description": "First test task",
        "user_id": 1
    }
    
    task_data_2 = {
        "title": "Second Task", 
        "description": "Second test task",
        "user_id": 1
    }
    
    client.post("/api/tasks/", json=task_data_1)
    client.post("/api/tasks/", json=task_data_2)
    
    # Retrieve all tasks for user 1
    response = client.get("/api/tasks/?user_id=1")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= 2  # At least the 2 tasks we created plus possibly others


def test_update_task(client: TestClient, session: Session):
    """Test updating a task"""
    # First create a task
    task_data = {
        "title": "Original Task",
        "description": "Original description",
        "user_id": 1
    }
    
    create_response = client.post("/api/tasks/", json=task_data)
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Then update it
    update_data = {
        "title": "Updated Task",
        "description": "Updated description"
    }
    
    response = client.put(f"/api/tasks/{task_id}?user_id=1", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated description"


def test_delete_task(client: TestClient, session: Session):
    """Test deleting a task"""
    # First create a task
    task_data = {
        "title": "Delete Test Task",
        "description": "Task for delete test",
        "user_id": 1
    }
    
    create_response = client.post("/api/tasks/", json=task_data)
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Then delete it
    response = client.delete(f"/api/tasks/{task_id}?user_id=1")
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/api/tasks/{task_id}?user_id=1")
    assert get_response.status_code == 404


def test_toggle_task_completion(client: TestClient, session: Session):
    """Test toggling task completion status"""
    # First create a task
    task_data = {
        "title": "Toggle Test Task",
        "description": "Task for toggle test",
        "user_id": 1
    }
    
    create_response = client.post("/api/tasks/", json=task_data)
    assert create_response.status_code == 200
    created_task = create_response.json()
    task_id = created_task["id"]
    
    # Initially should be false
    assert created_task["completed"] is False
    
    # Toggle to true
    toggle_data = {"completed": True}
    response = client.patch(f"/api/tasks/{task_id}/toggle-complete?user_id=1", json=toggle_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["completed"] is True
    
    # Toggle back to false
    toggle_data = {"completed": False}
    response = client.patch(f"/api/tasks/{task_id}/toggle-complete?user_id=1", json=toggle_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["completed"] is False


def test_filter_tasks_by_completion_status(client: TestClient, session: Session):
    """Test filtering tasks by completion status"""
    # Create a completed task
    completed_task_data = {
        "title": "Completed Task",
        "description": "This task is completed",
        "user_id": 1
    }
    
    create_response = client.post("/api/tasks/", json=completed_task_data)
    assert create_response.status_code == 200
    completed_task = create_response.json()
    task_id = completed_task["id"]
    
    # Toggle it to completed
    toggle_data = {"completed": True}
    client.patch(f"/api/tasks/{task_id}/toggle-complete?user_id=1", json=toggle_data)
    
    # Create an incomplete task
    incomplete_task_data = {
        "title": "Incomplete Task",
        "description": "This task is not completed",
        "user_id": 1
    }
    
    client.post("/api/tasks/", json=incomplete_task_data)
    
    # Get only completed tasks
    response = client.get("/api/tasks/?user_id=1&completed=true")
    assert response.status_code == 200
    completed_tasks = response.json()
    completed_titles = [task["title"] for task in completed_tasks]
    assert "Completed Task" in completed_titles
    
    # Get only incomplete tasks
    response = client.get("/api/tasks/?user_id=1&completed=false")
    assert response.status_code == 200
    incomplete_tasks = response.json()
    incomplete_titles = [task["title"] for task in incomplete_tasks]
    assert "Incomplete Task" in incomplete_titles