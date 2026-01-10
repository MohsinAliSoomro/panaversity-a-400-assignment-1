# Task Management API

A simple Task Management REST API built with FastAPI, SQLAlchemy, and Neon PostgreSQL database.

## Demo Video

[![Watch the demo video](https://cdn.loom.com/sessions/thumbnails/ab8edbf88919408b9a9655b360c1b4a9-with-play.jpg)](https://www.loom.com/share/ab8edbf88919408b9a9655b360c1b4a9)

## Features

- Create, read, update, and delete tasks
- Task priorities: low, medium, high, urgent
- Mark tasks as completed
- Built with FastAPI (modern, fast web framework)
- PostgreSQL database hosted on Neon
- Automatic API documentation (Swagger UI & ReDoc)

## Tech Stack & Packages Used

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi[standard] | >=0.128.0 | Modern, fast web framework for building APIs |
| uvicorn[standard] | - | ASGI server for running FastAPI |
| sqlalchemy | >=2.0.0 | SQL toolkit and ORM |
| psycopg2-binary | - | PostgreSQL database adapter |
| python-dotenv | - | Load environment variables from .env |
| pydantic | - | Data validation using Python type hints |
| pytest | >=9.0.2 | Testing framework |
| httpx | - | Async HTTP client for testing |
| alembic | - | Database migration tool |

## Prerequisites

- Python 3.8 or higher
- A Neon PostgreSQL database account (free tier available)
- Virtual environment (optional but recommended)

## Setup

### 1. Clone or navigate to the project

```bash
cd panaversity-a-400-assignment-1
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root with your Neon database URL:

```env
DATABASE_URL="postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require&channel_binding=require"
```

You can get your Neon database URL from the Neon dashboard.

### 6. Run the application

```bash
# Using uvicorn directly
uvicorn main:app --reload

# Or using the main.py script
python main.py
```

The API will be available at `http://127.0.0.1:8000`

### 7. Access API Documentation

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API health check |
| `POST` | `/tasks/` | Create a new task |
| `GET` | `/tasks/` | Get all tasks (with pagination) |
| `GET` | `/tasks/{task_id}` | Get a specific task |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `PATCH` | `/tasks/{task_id}/complete` | Mark task as completed |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

## Usage Examples

### Create a Task

```bash
curl -X POST "http://127.0.0.1:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write README and API docs",
    "priority": "high"
  }'
```

### Get All Tasks

```bash
curl -X GET "http://127.0.0.1:8000/tasks/"
```

### Get a Specific Task

```bash
curl -X GET "http://127.0.0.1:8000/tasks/1"
```

### Update a Task

```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "completed": true
  }'
```

### Mark Task as Completed

```bash
curl -X PATCH "http://127.0.0.1:8000/tasks/1/complete"
```

### Delete a Task

```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```

## Database Schema

### Tasks Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key (auto-increment) |
| title | String | Task title (required) |
| description | String | Task description (optional) |
| completed | Boolean | Task completion status |
| priority | Enum | low, medium, high, urgent |
| created_at | DateTime | Timestamp when task was created |
| updated_at | DateTime | Timestamp when task was last updated |

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

If you need to make schema changes:

```bash
# Generate a migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

### Database Connection Issues

- Verify your `DATABASE_URL` in `.env` file
- Ensure SSL mode is set to `require`
- Check that your Neon project is not paused

## License

This project is for educational purposes.
