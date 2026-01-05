name: neon-database
description: Comprehensive PostgreSQL database management with Neon, including connection setup, schema management, query optimization, and integration with Python frameworks like FastAPI. Use when working with Neon PostgreSQL databases for: (1) Setting up database connections, (2) Creating and managing database schemas, (3) Optimizing queries, (4) Integrating with Python web frameworks, (5) Managing connection pooling, or (6) Handling database migrations.
---

# Neon Database

## Overview

Neon is a serverless PostgreSQL database platform that provides a fully managed, auto-scaling PostgreSQL database service. This skill enables Claude to work effectively with Neon databases, providing guidance on connection setup, best practices, and integration with Python frameworks like FastAPI.

## Core Capabilities

### 1. Database Connection Setup
- Configure connection strings for Neon databases
- Set up SSL and authentication parameters
- Configure connection pooling for optimal performance

### 2. Framework Integration
- Integrate Neon with FastAPI using SQLAlchemy
- Set up async database sessions
- Configure proper error handling and connection management

### 3. Schema Management
- Create and manage database schemas
- Handle migrations and versioning
- Optimize table structures for Neon's architecture

### 4. Query Optimization
- Write efficient queries for Neon's serverless architecture
- Use connection pooling effectively
- Handle connection limits and timeouts

## Quick Start with FastAPI

To connect FastAPI to Neon:

1. Install required dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy asyncpg python-dotenv psycopg2-binary
   ```

2. Set up your database connection in a `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

3. Create a database.py file:
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
       echo=True,
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

   async def get_db():
       async with AsyncSessionLocal() as session:
           yield session
   ```

## Neon-Specific Considerations

### Connection Management
- Neon uses connection pooling by default
- Set appropriate pool sizes (typically smaller than traditional PostgreSQL)
- Use `pool_pre_ping=True` to validate connections before use
- Handle connection timeouts gracefully

### SSL Configuration
- Neon requires SSL connections
- Include `?sslmode=require` in your connection string
- No additional SSL certificate configuration needed

### Serverless Features
- Neon automatically scales compute resources
- Storage and compute are separated
- Use branching feature for isolated development environments
- Be aware of possible connection resets during scaling events

## Common Patterns

### Async Database Operations
```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()
```

### Error Handling
```python
from fastapi import HTTPException, status

async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user
```

## Migration with Alembic

For database schema management with Neon:

1. Initialize Alembic:
   ```bash
   pip install alembic
   alembic init alembic
   ```

2. Configure `alembic.ini` to use your async database URL

3. Generate and run migrations:
   ```bash
   alembic revision --autogenerate -m "Create users table"
   alembic upgrade head
   ```

## Troubleshooting

### Connection Issues
- Verify your connection string format
- Check that SSL mode is set to `require`
- Ensure your Neon project is not in idle state (it may pause after inactivity)

### Performance Issues
- Adjust connection pool settings based on your application's needs
- Use appropriate indexing strategies
- Consider connection lifecycle management

## Resources

For more detailed information, see the following reference files:

- **neon_api_reference.md**: Comprehensive API reference and configuration details
- **fastapi_integration.md**: Detailed guide for integrating Neon with FastAPI applications
- **neon_database_setup.py**: Python script for testing connections and basic database operations

## Scripts

This skill includes utility scripts for common Neon database operations:

### neon_database_setup.py
A Python script that provides utilities for:
- Testing database connections
- Creating tables
- Running basic queries
- Inserting test data

To use the script:
```bash
python scripts/neon_database_setup.py
```
The script requires a DATABASE_URL environment variable to be set.
