# FastAPI Skill Documentation

## Overview
This skill provides comprehensive information and utilities for working with FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## What This Skill Provides

### 1. Information and Explanations
- FastAPI concepts, features, and best practices
- Performance benefits and use cases
- Comparison with other frameworks
- Security considerations

### 2. Code Examples
- Basic FastAPI application structure
- APIRouter usage patterns
- Pydantic model definitions
- Dependency injection examples
- Error handling patterns
- Background task implementations

### 3. Project Structure Templates
- Recommended directory organization
- Separation of concerns patterns
- Testing structure suggestions

### 4. Best Practices Guidance
- Performance optimization tips
- Security recommendations
- Code organization strategies
- Testing methodologies

## How to Use This Skill

### When to Use
Use this skill when you need:
- To understand FastAPI concepts or features
- Code examples for FastAPI implementations
- Best practices for FastAPI development
- Project structure recommendations
- Performance optimization strategies
- Security implementation guidance

### Example Queries
- "Explain FastAPI project structure"
- "Show me a FastAPI router example"
- "What are FastAPI best practices?"
- "How do I implement authentication in FastAPI?"
- "Generate a FastAPI CRUD example"
- "What are the performance benefits of FastAPI?"

## Key Components

### fastapi_utils.py
A utility module containing:
- Project structure representations
- Code example generators
- Best practices information
- Helper functions for common tasks

### example_app.py
A complete example FastAPI application demonstrating:
- CRUD operations
- Pydantic model usage
- Dependency injection
- Background tasks
- Error handling
- Path/query parameter validation

### README.md
Detailed documentation about FastAPI including:
- Features and benefits
- Use cases
- Project structure
- Best practices
- APIRouter usage

## FastAPI Key Features

### Performance
- Very high performance, on par with NodeJS and Go
- Based on Starlette and Pydantic
- One of the fastest Python frameworks available

### Developer Experience
- Automatic validation and serialization
- Automatic interactive API documentation (Swagger UI and ReDoc)
- Full OpenAPI and JSON Schema compatibility
- Great editor support with completion everywhere

### Type Safety
- Based on standard Python type hints
- Automatic validation based on type annotations
- Runtime error prevention

### Asynchronous Support
- Built-in async/await support
- Handle many concurrent requests efficiently
- Non-blocking I/O operations

## Common Patterns

### APIRouter Organization
```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    return [{"name": "John", "id": 1}]
```

### Pydantic Models
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
```

### Dependency Injection
```python
from fastapi import Depends

def get_current_user():
    # Implementation
    return user

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return current_user
```

## Best Practices

1. Use Pydantic models for request/response validation
2. Implement proper error handling with HTTPException
3. Organize endpoints with APIRouter
4. Use dependency injection for shared functionality
5. Write comprehensive tests using pytest
6. Use environment variables for configuration
7. Implement proper authentication and authorization
8. Use async/await for I/O bound operations
9. Implement caching for expensive operations
10. Use background tasks for non-critical operations

## Performance Tips

- Use async/await for I/O bound operations
- Implement caching for expensive operations
- Use database connection pooling
- Optimize database queries with proper indexing
- Use pagination for large datasets
- Implement proper request/response validation to prevent unnecessary processing

## Security Considerations

- Implement proper authentication (OAuth2, JWT, etc.)
- Validate and sanitize all inputs
- Use HTTPS in production
- Implement rate limiting
- Protect against common vulnerabilities (XSS, CSRF, etc.)
- Use secure session management