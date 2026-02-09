from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from main import app
from src.database import get_session
from src.models.task import Task


def test_basic_functionality():
    """Basic test to verify the app works"""
    # Create an in-memory SQLite database for testing
    from sqlmodel import create_engine
    from src.models.task import Task
    test_engine = create_engine("sqlite://", 
                                connect_args={"check_same_thread": False},
                                poolclass=StaticPool)
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        def get_session_override():
            return session

        from src.database import get_session
        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)
        
        # Test the root endpoint
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to the Todo Task Management API"
        print("[PASS] Root endpoint test passed")

        # Test creating a task
        task_data = {
            "title": "Test Task",
            "description": "This is a test task"
        }

        response = client.post("/api/1/tasks/", json=task_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "This is a test task"
        assert data["user_id"] == 1
        assert data["completed"] is False
        assert "id" in data
        print("[PASS] Create task test passed")

        # Get the created task ID
        task_id = data["id"]

        # Test getting the task
        response = client.get(f"/api/1/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test Task"
        print("[PASS] Get task test passed")

        # Test getting all tasks for user
        response = client.get("/api/1/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        print("[PASS] Get all tasks test passed")

        # Test updating the task
        update_data = {
            "title": "Updated Test Task",
            "description": "This is an updated test task"
        }
        response = client.put(f"/api/1/tasks/{task_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Test Task"
        print("[PASS] Update task test passed")

        # Test toggling completion
        toggle_data = {"completed": True}
        response = client.patch(f"/api/1/tasks/{task_id}/complete", json=toggle_data)
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        print("[PASS] Toggle completion test passed")

        # Test deleting the task
        response = client.delete(f"/api/1/tasks/{task_id}")
        assert response.status_code == 200
        print("[PASS] Delete task test passed")

        # Verify the task is gone
        response = client.get(f"/api/1/tasks/{task_id}")
        assert response.status_code == 404
        print("[PASS] Verify deletion test passed")

        app.dependency_overrides.clear()
        print("\nAll tests passed! The task management system is working correctly.")


if __name__ == "__main__":
    test_basic_functionality()