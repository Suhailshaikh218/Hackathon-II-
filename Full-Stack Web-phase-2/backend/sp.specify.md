# Backend Specification Document

## Project Overview
A full-stack task management application with authentication, built using FastAPI, SQLModel, and Neon PostgreSQL. The backend provides a secure REST API for managing tasks with user authentication and authorization.

## Spec 1: Database Connection & Task Management

### Requirements Met
- ✅ Connected to Neon PostgreSQL database
- ✅ Created Task model with id, title, description, completed, created_at, updated_at fields
- ✅ Implemented CRUD operations for tasks
- ✅ Used SQLModel for database modeling
- ✅ Configured connection pooling and async operations

### Database Schema
```sql
-- Tasks table
CREATE TABLE task (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES user(id)
);

-- Users table
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints (Spec 1)
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

## Spec 2: Authentication & Security

### Requirements Met
- ✅ Created User model with id, email, hashed_password, and is_active fields
- ✅ Linked User model to Task model (One-to-Many relationship)
- ✅ Implemented JWT authentication using passlib and python-jose
- ✅ Created auth endpoints for signup and login
- ✅ Updated Task routes to require authentication and enforce user ownership

### Authentication Endpoints
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Authenticate user and return JWT token

### Security Features
- Password hashing using bcrypt via passlib
- JWT token-based authentication
- User-specific task access control
- Active user validation
- Secure token expiration

## Technical Architecture

### Tech Stack
- **Framework**: FastAPI
- **Database ORM**: SQLModel
- **Database**: Neon PostgreSQL
- **Authentication**: JWT with python-jose
- **Password Hashing**: passlib with bcrypt
- **Environment Management**: pydantic-settings

### Project Structure
```
backend/
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
├── src/
│   ├── __init__.py
│   ├── auth.py             # Authentication utilities
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database connection and setup
│   ├── services.py         # Business logic
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py         # User model
│   │   └── task.py         # Task model
│   └── api/
│       ├── __init__.py
│       ├── schemas/
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── auth.py     # Authentication routes
│       │   └── tasks.py    # Task management routes
```

### Modular Design
- **Separation of Concerns**: Models, routes, services, and authentication are in separate modules
- **Dependency Injection**: Database sessions injected into route handlers
- **Reusable Services**: Business logic abstracted into service functions
- **Configuration Management**: Centralized settings using pydantic-settings
- **Authentication Layer**: Separate auth module with reusable dependencies

## Database Configuration
- **Connection Pooling**: Configured for optimal performance
- **Async Operations**: All database operations are asynchronous
- **Migration Ready**: SQLModel supports Alembic for migrations
- **Environment Variables**: Database URL loaded from environment

## Error Handling
- **HTTP Exceptions**: Proper error codes and messages
- **Validation**: Pydantic models for request/response validation
- **Authentication Errors**: Specific handling for auth failures
- **Database Errors**: Proper exception handling for DB operations

## Security Measures
- **Input Validation**: All inputs validated through Pydantic models
- **SQL Injection Prevention**: SQLModel parameterized queries
- **Authentication**: JWT tokens with expiration
- **Authorization**: Per-user resource access control
- **Password Security**: Bcrypt hashing with salt

## API Documentation
- **Automatic Documentation**: Swagger UI and ReDoc available
- **Type Hints**: Full type annotations for all endpoints
- **Request/Response Models**: Defined with Pydantic
- **Endpoint Descriptions**: Detailed documentation for each endpoint

## Performance Considerations
- **Async Processing**: Non-blocking I/O operations
- **Connection Pooling**: Efficient database connection reuse
- **Indexing**: Proper database indexes on frequently queried fields
- **Caching**: Ready for integration with Redis or similar

## Testing Readiness
- **Modular Design**: Easy to unit test individual components
- **Dependency Injection**: Mockable dependencies for testing
- **Pydantic Models**: Validated data structures
- **Service Layer**: Isolated business logic for testing