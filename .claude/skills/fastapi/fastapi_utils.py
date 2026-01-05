"""
FastAPI Skill Utilities

This module provides utility functions and examples for working with FastAPI.
"""

from typing import Any, Dict, List, Optional
from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os


class FastAPIProjectStructure:
    """
    A class to represent the typical structure of a FastAPI project.
    """
    
    @staticmethod
    def get_typical_structure() -> Dict[str, Any]:
        """
        Returns a dictionary representing the typical structure of a FastAPI project.
        """
        return {
            "app": {
                "__init__.py": "Package initialization file",
                "main.py": "Application instance and configuration",
                "api": {
                    "__init__.py": "API package initialization",
                    "v1": {
                        "__init__.py": "API v1 package initialization",
                        "routers": {
                            "__init__.py": "Routers package initialization",
                            "users.py": "User-related endpoints",
                            "items.py": "Item-related endpoints",
                            "auth.py": "Authentication endpoints"
                        },
                        "dependencies.py": "Shared dependencies"
                    }
                },
                "models": {
                    "__init__.py": "Models package initialization",
                    "user.py": "User Pydantic models",
                    "item.py": "Item Pydantic models"
                },
                "schemas": {
                    "__init__.py": "Schemas package initialization",
                    "user.py": "User request/response schemas",
                    "item.py": "Item request/response schemas"
                },
                "database": {
                    "__init__.py": "Database package initialization",
                    "session.py": "Database session configuration",
                    "models.py": "ORM models"
                },
                "core": {
                    "__init__.py": "Core package initialization",
                    "config.py": "Application configuration",
                    "security.py": "Security utilities"
                },
                "utils": {
                    "__init__.py": "Utilities package initialization",
                    "helpers.py": "Helper functions"
                }
            },
            "tests": {
                "__init__.py": "Tests package initialization",
                "conftest.py": "Test configuration",
                "test_users.py": "User-related tests",
                "test_items.py": "Item-related tests"
            },
            "requirements.txt": "Project dependencies",
            "Dockerfile": "Containerization instructions",
            "README.md": "Project documentation"
        }


class FastAPIExampleGenerator:
    """
    A class to generate common FastAPI code examples.
    """
    
    @staticmethod
    def generate_basic_app() -> str:
        """
        Generates a basic FastAPI application example.
        """
        return '''
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI application"}
        '''.strip()
    
    @staticmethod
    def generate_router_example() -> str:
        """
        Generates an APIRouter example.
        """
        return '''
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    return [{"name": "John", "id": 1}]

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"name": "John", "id": user_id}
        '''.strip()
    
    @staticmethod
    def generate_pydantic_model_example() -> str:
        """
        Generates a Pydantic model example.
        """
        return '''
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

class UserCreate(User):
    password: str
        '''.strip()
    
    @staticmethod
    def generate_dependency_example() -> str:
        """
        Generates a dependency injection example.
        """
        return '''
from fastapi import Depends

def get_current_user():
    # Implementation to get current user
    return {"name": "John", "id": 1}

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return current_user
        '''.strip()


class FastAPIBestPractices:
    """
    A class containing FastAPI best practices.
    """
    
    @staticmethod
    def get_best_practices() -> List[str]:
        """
        Returns a list of FastAPI best practices.
        """
        return [
            "Use Pydantic models for request/response validation",
            "Implement proper error handling with HTTPException",
            "Use dependency injection for shared functionality",
            "Organize endpoints with APIRouter",
            "Use environment variables for configuration",
            "Implement proper authentication and authorization",
            "Write comprehensive tests using pytest",
            "Use docstrings and proper type hints",
            "Use background tasks for non-critical operations",
            "Use async/await for I/O bound operations"
        ]
    
    @staticmethod
    def get_performance_tips() -> List[str]:
        """
        Returns a list of performance tips for FastAPI.
        """
        return [
            "Use async/await for I/O bound operations",
            "Implement caching for expensive operations",
            "Use database connection pooling",
            "Optimize database queries with proper indexing",
            "Use pagination for large datasets",
            "Implement proper request/response validation to prevent unnecessary processing"
        ]


def create_fastapi_app(title: str = "FastAPI Application", 
                      version: str = "1.0.0", 
                      description: Optional[str] = None) -> FastAPI:
    """
    Creates a FastAPI application with basic configuration.
    
    Args:
        title: The title of the API
        version: The version of the API
        description: Optional description of the API
    
    Returns:
        A configured FastAPI application instance
    """
    app = FastAPI(
        title=title,
        version=version,
        description=description
    )
    
    @app.get("/")
    def home():
        return {"message": f"Welcome to {title}"}
    
    return app


def add_cors_middleware(app: FastAPI, 
                       allow_origins: List[str] = None,
                       allow_credentials: bool = True,
                       allow_methods: List[str] = None,
                       allow_headers: List[str] = None) -> None:
    """
    Adds CORS middleware to a FastAPI application.
    
    Args:
        app: The FastAPI application instance
        allow_origins: List of origins to allow
        allow_credentials: Whether to allow credentials
        allow_methods: List of HTTP methods to allow
        allow_headers: List of headers to allow
    """
    from fastapi.middleware.cors import CORSMiddleware
    
    if allow_origins is None:
        allow_origins = ["*"]
    if allow_methods is None:
        allow_methods = ["GET", "POST", "PUT", "DELETE"]
    if allow_headers is None:
        allow_headers = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
    )


# Example usage
if __name__ == "__main__":
    # Create a sample FastAPI app
    app = create_fastapi_app(
        title="Sample API",
        description="This is a sample FastAPI application"
    )
    
    # Add CORS middleware
    add_cors_middleware(app)
    
    # Print project structure
    structure = FastAPIProjectStructure.get_typical_structure()
    print("Typical FastAPI Project Structure:")
    for key, value in structure.items():
        print(f"- {key}")