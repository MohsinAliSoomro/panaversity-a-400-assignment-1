# Neon Database API Reference

## Connection String Format

The Neon database URL follows this format:
```
postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

### Components
- **username**: Your Neon database username
- **password**: Your Neon database password
- **ep-xxx.region.aws.neon.tech**: Your Neon endpoint
- **dbname**: Your database name
- **sslmode=require**: Required for secure connection

## SQLAlchemy Async Configuration

### Engine Parameters
- **pool_size**: Number of connections to maintain in the pool (default: 5)
- **max_overflow**: Additional connections beyond pool_size (default: 10)
- **pool_pre_ping**: Verify connections before use (recommended: True)
- **echo**: Log SQL statements (default: False, set True for debugging)

### Connection Pooling Considerations
- Neon handles connection pooling at the platform level
- Use smaller pool sizes than traditional PostgreSQL (5-10 vs 20+)
- Set `pool_pre_ping=True` to handle connection resets gracefully
- Consider connection timeouts during scaling events

## Neon-Specific Features

### Branching
- Neon allows creating isolated database branches
- Use branches for development, testing, and staging environments
- Branches share the same storage but have separate compute resources

### Serverless Scaling
- Compute resources automatically scale up and down based on demand
- Storage and compute are billed separately
- Connections may be reset during scaling events
- Implement retry logic for critical operations

### Connection Limits
- Neon has connection limits based on your plan
- Free tier: 5 connections
- Pro tier: 20 connections
- Scale tier: 100 connections

## Migration Best Practices

### Alembic Configuration
```python
# alembic.ini
sqlalchemy.url = postgresql+asyncpg://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
```

### Migration Commands
```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Check current revision
alembic current
```

## Error Handling

### Common Neon-Specific Errors
- **Connection timeout**: Handle with retry logic and appropriate timeouts
- **Connection reset**: Use `pool_pre_ping=True` and implement reconnection logic
- **Idle timeout**: Neon may pause compute after inactivity; first connection after pause may be slow

### Recommended Error Handling Pattern
```python
import asyncio
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.pool import Pool

# Configure engine with proper error handling
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections every 5 minutes
    poolclass=QueuePool
)

# Implement retry logic for critical operations
async def execute_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except DisconnectionError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Performance Optimization

### Query Optimization
- Use indexes appropriately for frequently queried columns
- Limit result sets with OFFSET and LIMIT
- Use connection pooling effectively
- Consider read replicas for read-heavy workloads

### Connection Management
- Use async sessions for non-blocking operations
- Implement proper session lifecycle management
- Close sessions properly to return connections to the pool
- Monitor connection usage and adjust pool sizes as needed