import requests

class Tools:
    @staticmethod
    def create_user(email: str, password: str):
        """Create a new user
        
        Args:
            email (str): The email of the user
            password (str): The password of the user
        """
        response = requests.post("http://127.0.0.1:8000/users/register", json={"email": email, "password": password})
        return response.json()

    @staticmethod
    def login(email: str, password: str):
        """Login a user
        
        Args:
            email (str): The email of the user
            password (str): The password of the user
        """
        response = requests.post("http://127.0.0.1:8000/users/login", data={"username": email, "password": password})
        return response.json()
    
    @staticmethod
    def create_task(token: str, title: str, description: str, priority: str = "medium", owner: int = 1):
        """Create a new task
        
        Args:
            token (str): The token of the user
            title (str): The title of the task
            description (str): The description of the task
            priority (str): The priority of the task
            owner (int): The owner id of the task
        """
        data = {
            "title": title,
            "description": description,
            "priority": priority,
            "owner": owner
        }
        response = requests.post("http://127.0.0.1:8000/tasks", json=data, headers={"Authorization": f"Bearer {token}"})
        return response.json()
    
    @staticmethod
    def get_tasks(token: str):
        """Get all tasks
        
        Args:
            token (str): The token of the user
        """
        response = requests.get("http://127.0.0.1:8000/tasks", headers={"Authorization": f"Bearer {token}"})
        return response.json()
    
    @staticmethod
    def update_task(token: str, task_id: int, title: str = None, description: str = None, priority: str = None):
        """Update a task
        
        Args:
            token (str): The token of the user
            task_id (int): The id of the task
            title (str): The title of the task
            description (str): The description of the task
            priority (str): The priority of the task
        """
        data = {}
        if title: data["title"] = title
        if description: data["description"] = description
        if priority: data["priority"] = priority

        response = requests.put(f"http://127.0.0.1:8000/tasks/{task_id}", json=data, headers={"Authorization": f"Bearer {token}"})
        return response.json()
    
    @staticmethod
    def delete_task(token: str, task_id: int):
        """Delete a task
        
        Args:
            token (str): The token of the user
            task_id (int): The id of the task
        """
        response = requests.delete(f"http://127.0.0.1:8000/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
        return response.json()


# response = Tools.login("mohsin@gmail.com", "Test@123")
# print(response)
# response = Tools.get_tasks("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtb2hzaW5AZ21haWwuY29tIiwiZXhwIjoxNzY4NDAwNTgzfQ.f6fp_BTUQ3txdVPXRxdC7lOxvwRzw33Xoufx3C9Pzt0")
# print(response)