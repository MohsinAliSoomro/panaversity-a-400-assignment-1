# Neon Database with FastAPI Integration Guide

## FastAPI Setup with Neon

### Required Dependencies
```bash
pip install fastapi uvicorn sqlalchemy asyncpg python-dotenv psycopg2-binary
```

### Database Configuration
Create a `database.py` file with the following configuration:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for debugging
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,  # Initial connection pool size
    max_overflow=10  # Additional connections beyond pool_size
)

AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

## Model Definition

### Example User Model
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

## API Endpoints

### Example FastAPI Endpoints
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
from database import get_db, engine
from models import Base, User as UserModel

# Create database tables on startup
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(title="FastAPI with Neon", on_startup=[create_tables])

# Pydantic models for request/response
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = UserModel(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).offset(skip).limit(limit))
    users = result.scalars().all()
    return users
```

## Environment Configuration

### .env File
```
DATABASE_URL=postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

## Connection Management Best Practices

### Session Management
- Always use dependency injection for database sessions
- Use `async with` statements for proper session lifecycle
- Never forget to commit transactions when making changes
- Handle exceptions properly to ensure sessions are closed

### Error Handling
```python
from fastapi import HTTPException, status

async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user
```

## Deployment Considerations

### Production Settings
- Set `echo=False` in production to avoid logging SQL statements
- Adjust pool sizes based on expected load
- Implement proper logging and monitoring
- Use environment variables for configuration
- Consider using a process manager like Gunicorn for production

### Neon-Specific Deployment
- Be aware of Neon's connection limits based on your plan
- Implement retry logic for connection failures
- Monitor connection usage and adjust pool sizes accordingly
- Consider using Neon's branching feature for development/staging environments