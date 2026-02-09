# Backend API Documentation

## Project Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Neon PostgreSQL account and database

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend root directory with the following variables:
```env
DATABASE_URL=postgresql://<username>:<password>@ep-<endpoint>.us-east-1.aws.neon.tech/<database_name>?sslmode=require
SECRET_KEY=your-super-secret-key-for-production-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

Access the automatic API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication Endpoints

#### POST /api/auth/signup
Register a new user

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T12:00:00Z"
}
```

#### POST /api/auth/login
Authenticate user and receive JWT token

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_active": true,
    "created_at": "2023-10-01T12:00:00Z",
    "updated_at": "2023-10-01T12:00:00Z"
  }
}
```

### Task Management Endpoints

All task endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

#### POST /api/{user_id}/tasks
Create a new task

**Path Parameter:**
- `user_id` (integer): The ID of the user creating the task

**Request Body:**
```json
{
  "title": "Sample Task",
  "description": "Task description here",
  "completed": false
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "Task description here",
  "completed": false,
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T12:00:00Z",
  "user_id": 1
}
```

#### GET /api/{user_id}/tasks
Get all tasks for a specific user

**Path Parameter:**
- `user_id` (integer): The ID of the user whose tasks to retrieve

**Query Parameters:**
- `completed` (boolean, optional): Filter by completion status

**Response:**
```json
[
  {
    "id": 1,
    "title": "Sample Task",
    "description": "Task description here",
    "completed": false,
    "created_at": "2023-10-01T12:00:00Z",
    "updated_at": "2023-10-01T12:00:00Z",
    "user_id": 1
  }
]
```

#### GET /api/{user_id}/tasks/{task_id}
Get a specific task

**Path Parameters:**
- `user_id` (integer): The ID of the user
- `task_id` (integer): The ID of the task

**Response:**
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "Task description here",
  "completed": false,
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T12:00:00Z",
  "user_id": 1
}
```

#### PUT /api/{user_id}/tasks/{task_id}
Update a task

**Path Parameters:**
- `user_id` (integer): The ID of the user
- `task_id` (integer): The ID of the task

**Request Body:**
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T13:00:00Z",
  "user_id": 1
}
```

#### PATCH /api/{user_id}/tasks/{task_id}/complete
Toggle task completion status

**Path Parameters:**
- `user_id` (integer): The ID of the user
- `task_id` (integer): The ID of the task

**Request Body:**
```json
{
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "Task description here",
  "completed": true,
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T13:00:00Z",
  "user_id": 1
}
```

#### DELETE /api/{user_id}/tasks/{task_id}
Delete a task

**Path Parameters:**
- `user_id` (integer): The ID of the user
- `task_id` (integer): The ID of the task

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (required)
- `SECRET_KEY`: Secret key for JWT signing (required)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## Database Initialization

On startup, the application automatically creates the required tables if they don't exist. The database schema includes:

- `user` table: Stores user information with authentication details
- `task` table: Stores task information linked to users

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource successfully created
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Security Features

- JWT-based authentication with configurable expiration
- Passwords are hashed using bcrypt
- Input validation through Pydantic models
- SQL injection prevention through parameterized queries
- User isolation - users can only access their own tasks