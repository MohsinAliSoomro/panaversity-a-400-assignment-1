import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import StaticPool
from main import app, get_db, Base, TaskDB
from main import TaskCreate, TaskUpdate
import asyncio

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Override the database dependency
async def override_get_db():
    async with AsyncSession(engine) as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as client:
        yield client

def test_create_task(test_client):
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    
    response = test_client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["completed"] is False
    assert "id" in data

def test_get_tasks(test_client):
    """Test getting all tasks"""
    # First create a task
    task_data = {
        "title": "Get Tasks Test",
        "description": "Test for getting tasks"
    }
    test_client.post("/tasks/", json=task_data)
    
    # Then get all tasks
    response = test_client.get("/tasks/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= 1
    assert any(task["title"] == "Get Tasks Test" for task in data)

def test_get_task_by_id(test_client):
    """Test getting a specific task by ID"""
    # Create a task first
    task_data = {
        "title": "Specific Task",
        "description": "Test for getting specific task"
    }
    create_response = test_client.post("/tasks/", json=task_data)
    assert create_response.status_code == 201
    
    task_id = create_response.json()["id"]
    
    # Get the task by ID
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"

def test_get_task_not_found(test_client):
    """Test getting a task that doesn't exist"""
    response = test_client.get("/tasks/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_update_task(test_client):
    """Test updating an existing task"""
    # Create a task first
    task_data = {
        "title": "Original Task",
        "description": "Original description"
    }
    create_response = test_client.post("/tasks/", json=task_data)
    assert create_response.status_code == 201
    
    task_id = create_response.json()["id"]
    
    # Update the task
    update_data = {
        "title": "Updated Task",
        "completed": True
    }
    response = test_client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Task"
    assert data["completed"] is True

def test_update_task_not_found(test_client):
    """Test updating a task that doesn't exist"""
    update_data = {
        "title": "Updated Task",
        "completed": True
    }
    response = test_client.put("/tasks/99999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_delete_task(test_client):
    """Test deleting an existing task"""
    # Create a task first
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted"
    }
    create_response = test_client.post("/tasks/", json=task_data)
    assert create_response.status_code == 201
    
    task_id = create_response.json()["id"]
    
    # Verify the task exists
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Delete the task
    response = test_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify the task is deleted
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_delete_task_not_found(test_client):
    """Test deleting a task that doesn't exist"""
    response = test_client.delete("/tasks/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_create_task_minimal_data(test_client):
    """Test creating a task with minimal data (only required fields)"""
    task_data = {
        "title": "Minimal Task"
        # No description provided (should be optional)
    }
    
    response = test_client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["description"] is None
    assert data["completed"] is False

def test_root_endpoint(test_client):
    """Test the root endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "Task Management API" in data["message"]
    assert "status" in data
    assert data["status"] == "running"