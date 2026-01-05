import pytest
from main import TaskPriority

def test_create_task(test_client):
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "high"
    }

    response = test_client.post("/tasks/", json=task_data)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["priority"] == "high"
    assert data["completed"] is False
    assert "id" in data

def test_get_tasks(test_client):
    """Test getting all tasks"""
    # First create a task
    task_data = {
        "title": "Get Tasks Test",
        "description": "Test for getting tasks",
        "priority": "medium"
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
        "description": "Test for getting specific task",
        "priority": "urgent"
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
    assert data["priority"] == "urgent"

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
        "description": "Original description",
        "priority": "low"
    }
    create_response = test_client.post("/tasks/", json=task_data)
    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Task",
        "completed": True,
        "priority": "high"
    }
    response = test_client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Task"
    assert data["completed"] is True
    assert data["priority"] == "high"

def test_update_task_not_found(test_client):
    """Test updating a task that doesn't exist"""
    update_data = {
        "title": "Updated Task",
        "completed": True
    }
    response = test_client.put("/tasks/99999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_complete_task(test_client):
    """Test marking a task as complete"""
    # Create a task first
    task_data = {
        "title": "Task to Complete",
        "description": "This task will be completed",
        "priority": "medium"
    }
    create_response = test_client.post("/tasks/", json=task_data)
    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Complete the task
    response = test_client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["completed"] is True
    assert data["updated_at"] is not None

def test_complete_already_completed_task(test_client):
    """Test completing an already completed task"""
    # Create and complete a task
    task_data = {
        "title": "Task to Complete",
        "description": "This task will be completed",
        "priority": "medium"
    }
    create_response = test_client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Complete it first time
    test_client.patch(f"/tasks/{task_id}/complete")

    # Try to complete it again
    response = test_client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 400
    assert "already completed" in response.json()["detail"].lower()

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
        # No description or priority provided (should use defaults)
    }

    response = test_client.post("/tasks/", json=task_data)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["description"] is None
    assert data["priority"] == "medium"  # Default priority
    assert data["completed"] is False

def test_create_task_with_all_priorities(test_client):
    """Test creating tasks with all priority levels"""
    priorities = ["low", "medium", "high", "urgent"]

    for priority in priorities:
        task_data = {
            "title": f"{priority.capitalize()} Priority Task",
            "priority": priority
        }
        response = test_client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        assert response.json()["priority"] == priority

def test_root_endpoint(test_client):
    """Test the root endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "Task Management API" in data["message"]
    assert "status" in data
    assert data["status"] == "running"
