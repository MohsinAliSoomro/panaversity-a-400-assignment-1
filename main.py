from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine, Enum as SQLEnum
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./tasks.db")  # Fallback to SQLite for development

# For Neon/PostgreSQL, use async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
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

# Priority Enum
class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# Database Models
class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Pydantic Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[TaskPriority] = None

class Task(TaskBase):
    id: int
    completed: bool
    priority: TaskPriority
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Create tables on startup
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# FastAPI app
app = FastAPI(
    title="Task Management API",
    description="A simple task management API with CRUD operations",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await create_tables()

# CRUD Endpoints
@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import insert

    db_task = TaskDB(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@app.get("/tasks/", response_model=List[Task])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select

    result = await db.execute(select(TaskDB).offset(skip).limit(limit))
    tasks = result.scalars().all()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select

    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select, update

    # Get the existing task
    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Update only the fields that were provided
    update_data = task_update.dict(exclude_unset=True)
    if not update_data:
        # If no fields to update, return the existing task
        return db_task

    await db.execute(
        update(TaskDB)
        .where(TaskDB.id == task_id)
        .values(**update_data)
    )
    await db.commit()

    # Refresh and return the updated task
    await db.refresh(db_task)
    return db_task

@app.patch("/tasks/{task_id}/complete", response_model=Task)
async def complete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select, update

    # Get the existing task
    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Check if task is already completed
    if db_task.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Task with id {task_id} is already completed"
        )

    # Mark task as completed
    await db.execute(
        update(TaskDB)
        .where(TaskDB.id == task_id)
        .values(completed=True)
    )
    await db.commit()

    # Refresh and return the updated task
    await db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select, delete

    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    await db.execute(delete(TaskDB).where(TaskDB.id == task_id))
    await db.commit()

@app.get("/")
def read_root():
    return {"message": "Task Management API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
