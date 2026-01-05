# FastAPI Skill

## Overview
This skill provides comprehensive information and utilities for working with FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Purpose
The FastAPI skill enables Claude to:
- Explain FastAPI concepts, features, and best practices
- Provide code examples for common FastAPI patterns
- Describe typical project structures for FastAPI applications
- Offer guidance on API design and implementation
- Share information about FastAPI's performance benefits and use cases

## Key Features of FastAPI

### Performance
- Very high performance, on par with NodeJS and Go
- One of the fastest Python frameworks available (based on Starlette and Pydantic)
- Independent TechEmpower benchmarks show FastAPI as one of the fastest Python frameworks

### Development Benefits
- **Fast to code**: Increase development speed by 200-300%
- **Fewer bugs**: Reduce 40% of human-induced errors
- **Intuitive**: Great editor support with completion everywhere
- **Easy to use**: Designed for easy learning and use
- **Short**: Minimize code duplication with multiple features per parameter declaration
- **Robust**: Production-ready code with automatic interactive documentation

### Technical Features
- Based on standard Python type hints
- Automatic validation and serialization
- Automatic interactive API documentation (Swagger UI and ReDoc)
- Full OpenAPI and JSON Schema compatibility
- Built-in asynchronous support
- Dependency injection system
- Security features (OAuth2, JWT, HTTP Basic auth)

## Typical Project Structure

A typical FastAPI project follows a modular structure:

```
my_fastapi_app/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application instance and configuration
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── v1/              # Version 1 of the API
│   │   │   ├── __init__.py
│   │   │   ├── routers/     # API routers
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   │   ├── items.py
│   │   │   │   └── auth.py
│   │   │   └── dependencies.py  # Shared dependencies
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/             # Request/Response schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── database/            # Database configuration
│   │   ├── __init__.py
│   │   ├── session.py
│   │   └── models.py        # ORM models
│   ├── core/                # Core configurations
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── tests/                   # Test files
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## APIRouter Usage

APIRouter is a powerful feature that allows you to organize your application's endpoints into separate modules:

```python
# app/api/v1/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.api.v1.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100):
    # Implementation here
    pass

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Implementation here
    pass

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int):
    # Implementation here
    pass
```

## Common Use Cases

FastAPI is used by major companies for various applications:
- **Microsoft**: ML services integrated into Windows and Office products
- **Uber**: REST server for Ludwig (prediction queries)
- **Netflix**: Crisis management orchestration framework (Dispatch)
- **Cisco**: Production APIs, Virtual TAC Engineer services
- **Explosion AI**: APIs for spaCy (NLP library)

Typical use cases include:
- Building REST APIs
- ML services and prediction endpoints
- Production-ready web APIs
- Microservices
- GraphQL APIs
- WebSocket applications
- Data science APIs
- Real-time applications with WebSocket support
- Authentication services
- File upload/download services
- Background task processing

## Best Practices

1. **Use Pydantic Models**: Always use Pydantic models for request/response validation
2. **Implement Proper Error Handling**: Use HTTPException for proper error responses
3. **Use Dependency Injection**: Leverage FastAPI's dependency injection system
4. **Organize with APIRouter**: Use routers to separate different parts of your API
5. **Environment Configuration**: Use environment variables for configuration
6. **Security First**: Implement proper authentication and authorization
7. **Testing**: Write comprehensive tests using pytest
8. **Documentation**: Use docstrings and proper type hints for better documentation
9. **Background Tasks**: Use background tasks for non-critical operations
10. **Performance**: Use async/await for I/O bound operations and consider caching for expensive operations