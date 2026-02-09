# Todo Task Management API - Modular Architecture

This is a FastAPI-based task management system with a modular architecture following industry best practices.

## Project Structure

```
backend/
├── main.py                 # Main application entry point
├── .env                    # Environment variables
├── requirements.txt        # Dependencies
├── simple_test.py          # Basic functionality tests
├── test_main.py            # Comprehensive tests
└── src/                   # Source code directory
    ├── __init__.py
    ├── config.py          # Configuration and settings
    ├── database.py        # Database connection and session management
    ├── services.py        # Business logic layer
    ├── models/            # Database models
    │   ├── __init__.py
    │   └── task.py        # Task model definitions
    └── api/               # API layer
        ├── __init__.py
        ├── routes/        # API route handlers
        │   ├── __init__.py
        │   └── tasks.py   # Task-related routes
        └── schemas/       # API schemas (Pydantic models)
            ├── __init__.py
            └── task.py    # Task-related schemas
```

## Features

- **Create Task**: Create a new task with required title and optional description
- **List Tasks**: Retrieve all tasks for a given user_id with optional filtering by completion status
- **Retrieve Task**: Get task details by task ID
- **Update Task**: Modify task fields (title, description, completed)
- **Delete Task**: Permanently remove a task
- **Toggle Completion**: Dedicated endpoint to toggle task completion status

## Data Model

The system uses a SQLModel-based Task model with the following fields:

- `id`: Integer, primary key
- `user_id`: Integer, indexed for performance (foreign key to user)
- `title`: String, required (1-200 characters)
- `description`: String, optional (up to 1000 characters)
- `completed`: Boolean, default False, indexed for filtering
- `created_at`: DateTime, server-generated timestamp
- `updated_at`: DateTime, server-generated timestamp

## API Endpoints

### POST `/api/{user_id}/tasks`
Create a new task with required title and optional description

Request body:
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

Response: Task object with all fields

### GET `/api/{user_id}/tasks[?completed={true|false}]`
List all tasks for a given user_id, with optional filtering by completion status

Response: Array of Task objects

### GET `/api/{user_id}/tasks/{taskId}`
Retrieve a single task by ID for a specific user

Response: Task object

### PUT `/api/{user_id}/tasks/{taskId}`
Update task fields (title, description, completion state)

Request body:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

Response: Updated Task object

### DELETE `/api/{user_id}/tasks/{taskId}`
Delete a task permanently

Response: Success message

### PATCH `/api/{user_id}/tasks/{taskId}/complete`
Toggle task completion state

Request body:
```json
{
  "completed": true
}
```

Response: Updated Task object

## Database Configuration

The application connects to PostgreSQL using the `DATABASE_URL` from the `.env` file:

```
DATABASE_URL=postgresql://username:password@localhost/dbname
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your database configuration:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Testing

Run the simple test suite:
```bash
python simple_test.py
```

Or run the comprehensive tests:
```bash
python -m pytest test_main.py -v
```

## Key Implementation Notes

- All timestamps are generated server-side using UTC
- Database-level indexes on `user_id` and `completed` fields for optimal query performance
- Strict user isolation - all queries are filtered by user_id
- Proper REST semantics followed throughout
- Pydantic models used for request/response validation
- Modular architecture separating concerns (models, services, routes, schemas)