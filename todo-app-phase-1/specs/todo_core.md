# Todo Core Specification

## Overview
Core functionality for a todo application that allows users to manage their tasks with in-memory storage.

## Features

### 1. Add Task
- Accept a title (required), description (optional), priority (optional, default: Medium), category (optional), due date (optional, format: YYYY-MM-DD), and recurring pattern (optional, values: Daily/Weekly/Monthly)
- Assign a unique auto-incrementing ID to each task
- Set initial status to 'pending'
- Store creation timestamp
- Return the created task with all details

### 2. View All Tasks
- Display all tasks in the system
- Show task ID, title, description, status, priority, category, due date, recurring pattern, and creation timestamp
- Display status as either 'pending' or 'completed'
- Sort tasks by creation date (newest first)

### 3. Update Task
- Allow updating task title, description, priority, category, due date, and recurring pattern
- Prevent modification of task ID and creation timestamp
- Maintain current status unless explicitly changed
- Return updated task details

### 4. Delete Task
- Remove a specific task by its ID
- Return success/failure status
- Handle attempts to delete non-existent tasks gracefully

### 5. Mark Task as Completed
- Change task status from 'pending' to 'completed'
- Accept task ID as parameter
- Return success/failure status
- Handle attempts to mark non-existent tasks gracefully

## New Features

### 6. Task ID (Auto-increment)
- Each task gets a unique, auto-incrementing integer ID
- IDs are assigned sequentially starting from 1
- IDs are never reused after deletion

### 7. Priority Levels
- Tasks can have one of three priority levels: High, Medium, Low
- Default priority is Medium if not specified
- Priority affects task sorting and display

### 8. Category (Optional)
- Tasks can be assigned to an optional category
- Categories are user-defined strings
- Tasks without a category have an empty or null category field

### 9. Due Date (YYYY-MM-DD)
- Tasks can have an optional due date in YYYY-MM-DD format
- Due dates are validated to ensure they are in the correct format
- Tasks can be filtered by due date

### 10. Recurring Patterns
- Tasks can be set to repeat with the following patterns:
  - Daily: repeats every day
  - Weekly: repeats every week
  - Monthly: repeats every month
- Recurring tasks automatically generate new instances when completed
- Default is non-recurring if not specified

## Technical Requirements
- Use Python 3.13
- Use in-memory storage (no database)
- Include type hints throughout the code
- Follow clean code principles
- Implement proper error handling

## Data Model
- Task: {id: int, title: str, description: str, status: str, priority: str, category: str, due_date: str, recurring_pattern: str, created_at: datetime, updated_at: datetime}
- Status values: 'pending', 'completed'
- Priority values: 'High', 'Medium', 'Low'
- Recurring pattern values: 'Daily', 'Weekly', 'Monthly', null

## Functions Required
- add_task(title: str, description: str = "", priority: str = "Medium", category: str = "", due_date: str = "", recurring_pattern: str = "") -> Task
- view_all_tasks() -> List[Task]
- update_task(task_id: int, title: str = None, description: str = None, priority: str = None, category: str = None, due_date: str = None, recurring_pattern: str = None) -> Optional[Task]
- delete_task(task_id: int) -> bool
- mark_task_completed(task_id: int) -> bool