# Todo App Specification

## Overview
A simple command-line todo application that allows users to manage their tasks with in-memory storage.

## Features
1. Add new tasks
2. List all tasks
3. Mark tasks as completed
4. Delete tasks
5. Clear all tasks

## Technical Requirements
- Use Python 3.13
- Use in-memory storage (no database)
- Include type hints throughout the code
- Follow clean code principles

## User Interface
- Command-line interface (CLI)
- Menu-driven options for task management
- Clear prompts and feedback messages

## Data Model
- Task: {id: int, title: str, completed: bool, created_at: datetime}
- TodoList: List of Task objects

## Functions Required
- add_task(title: str) -> int
- list_tasks() -> List[Task]
- mark_completed(task_id: int) -> bool
- delete_task(task_id: int) -> bool
- clear_all_tasks() -> None