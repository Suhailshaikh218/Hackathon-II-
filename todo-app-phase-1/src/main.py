#!/usr/bin/env python3
"""
Advanced Todo Application
A command-line Todo application with advanced features including priority, categories, due dates, and recurring tasks.
"""

import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class TodoItem:
    """Represents a single todo item"""
    
    def __init__(self, 
                 id: int,
                 title: str, 
                 description: str = "", 
                 completed: bool = False, 
                 created_at: str = None,
                 priority: str = "Medium",
                 category: str = "",
                 due_date: str = "",
                 recurring_pattern: str = ""):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority if priority in ["High", "Medium", "Low"] else "Medium"
        self.category = category
        self.due_date = due_date  # Format: YYYY-MM-DD
        self.recurring_pattern = recurring_pattern  # Daily, Weekly, Monthly
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert the todo item to a dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "category": self.category,
            "due_date": self.due_date,
            "recurring_pattern": self.recurring_pattern,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TodoItem':
        """Create a TodoItem from a dictionary"""
        item = cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False),
            created_at=data.get('created_at'),
            priority=data.get('priority', 'Medium'),
            category=data.get('category', ''),
            due_date=data.get('due_date', ''),
            recurring_pattern=data.get('recurring_pattern', '')
        )
        item.updated_at = data.get('updated_at', datetime.now().isoformat())
        return item

    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        priority_indicator = {"High": "!", "Medium": "~", "Low": "."}[self.priority]
        due_info = f" (Due: {self.due_date})" if self.due_date else ""
        category_info = f" [{self.category}]" if self.category else ""
        return f"[{status}]{priority_indicator} {self.title}{category_info}{due_info} - {self.description}"


class TodoManager:
    """Manages a collection of todo items"""
    
    def __init__(self, storage_file: str = "todos.json"):
        self.storage_file = storage_file
        self.todos: List[TodoItem] = []
        self.next_id = 1
        self.load_todos()
        self._update_next_id()

    def _update_next_id(self):
        """Update the next available ID based on existing todos"""
        if self.todos:
            self.next_id = max(todo.id for todo in self.todos) + 1
        else:
            self.next_id = 1

    def _validate_priority(self, priority: str) -> bool:
        """Validate priority value"""
        return priority in ["High", "Medium", "Low"]

    def _validate_date_format(self, date_str: str) -> bool:
        """Validate date format (YYYY-MM-DD)"""
        if not date_str:
            return True  # Empty date is valid
        return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_str))

    def _validate_recurring_pattern(self, pattern: str) -> bool:
        """Validate recurring pattern"""
        return pattern in ["", "Daily", "Weekly", "Monthly"]

    def add_todo(self, 
                 title: str, 
                 description: str = "", 
                 priority: str = "Medium", 
                 category: str = "", 
                 due_date: str = "", 
                 recurring_pattern: str = "") -> Optional[TodoItem]:
        """Add a new todo item"""
        # Validate inputs
        if not self._validate_priority(priority):
            print(f"Invalid priority: {priority}. Must be one of: High, Medium, Low")
            return None
        
        if not self._validate_date_format(due_date):
            print(f"Invalid date format: {due_date}. Expected format: YYYY-MM-DD")
            return None
        
        if not self._validate_recurring_pattern(recurring_pattern):
            print(f"Invalid recurring pattern: {recurring_pattern}. Must be one of: Daily, Weekly, Monthly, or empty")
            return None

        todo = TodoItem(
            id=self.next_id,
            title=title, 
            description=description, 
            priority=priority, 
            category=category, 
            due_date=due_date, 
            recurring_pattern=recurring_pattern
        )
        self.todos.append(todo)
        self.next_id += 1
        self.save_todos()
        return todo

    def remove_todo(self, todo_id: int) -> bool:
        """Remove a todo item by ID"""
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                self.save_todos()
                return True
        return False

    def toggle_completion(self, todo_id: int) -> bool:
        """Toggle the completion status of a todo item"""
        for todo in self.todos:
            if todo.id == todo_id:
                todo.completed = not todo.completed
                todo.updated_at = datetime.now().isoformat()
                
                # Handle recurring tasks
                if todo.completed and todo.recurring_pattern:
                    self._create_recurring_task(todo)
                
                self.save_todos()
                return True
        return False

    def _create_recurring_task(self, completed_todo: TodoItem):
        """Create a new task based on a recurring pattern when the original is completed"""
        if completed_todo.recurring_pattern == "Daily":
            next_due = (datetime.fromisoformat(completed_todo.due_date) + timedelta(days=1)).strftime('%Y-%m-%d') if completed_todo.due_date else ""
        elif completed_todo.recurring_pattern == "Weekly":
            next_due = (datetime.fromisoformat(completed_todo.due_date) + timedelta(weeks=1)).strftime('%Y-%m-%d') if completed_todo.due_date else ""
        elif completed_todo.recurring_pattern == "Monthly":
            # Simple monthly calculation (adding ~30 days)
            next_due = (datetime.fromisoformat(completed_todo.due_date) + timedelta(days=30)).strftime('%Y-%m-%d') if completed_todo.due_date else ""
        else:
            return  # No recurring pattern

        # Create a new task with the same properties but reset completion status
        new_todo = TodoItem(
            id=self.next_id,
            title=completed_todo.title,
            description=completed_todo.description,
            priority=completed_todo.priority,
            category=completed_todo.category,
            due_date=next_due,
            recurring_pattern=completed_todo.recurring_pattern
        )
        self.todos.append(new_todo)
        self.next_id += 1
        self.save_todos()

    def update_todo(self, 
                    todo_id: int, 
                    title: str = None, 
                    description: str = None,
                    priority: str = None,
                    category: str = None,
                    due_date: str = None,
                    recurring_pattern: str = None) -> bool:
        """Update a todo item"""
        for todo in self.todos:
            if todo.id == todo_id:
                if title is not None:
                    todo.title = title
                if description is not None:
                    todo.description = description
                if priority is not None:
                    if self._validate_priority(priority):
                        todo.priority = priority
                    else:
                        print(f"Invalid priority: {priority}. Must be one of: High, Medium, Low")
                        return False
                if category is not None:
                    todo.category = category
                if due_date is not None:
                    if self._validate_date_format(due_date):
                        todo.due_date = due_date
                    else:
                        print(f"Invalid date format: {due_date}. Expected format: YYYY-MM-DD")
                        return False
                if recurring_pattern is not None:
                    if self._validate_recurring_pattern(recurring_pattern):
                        todo.recurring_pattern = recurring_pattern
                    else:
                        print(f"Invalid recurring pattern: {recurring_pattern}. Must be one of: Daily, Weekly, Monthly, or empty")
                        return False
                
                todo.updated_at = datetime.now().isoformat()
                self.save_todos()
                return True
        return False

    def get_todo(self, todo_id: int) -> Optional[TodoItem]:
        """Get a todo item by ID"""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def list_todos(self, show_completed: bool = True, sort_by_priority: bool = False) -> List[TodoItem]:
        """List all todos, optionally filtering out completed ones"""
        if show_completed:
            todos = self.todos
        else:
            todos = [todo for todo in self.todos if not todo.completed]
        
        # Sort by priority if requested, otherwise by creation date (newest first)
        if sort_by_priority:
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            todos.sort(key=lambda x: (priority_order[x.priority], datetime.fromisoformat(x.created_at)), reverse=True)
        else:
            todos.sort(key=lambda x: datetime.fromisoformat(x.created_at), reverse=True)
        
        return todos

    def save_todos(self):
        """Save todos to the storage file"""
        with open(self.storage_file, 'w') as f:
            json.dump([todo.to_dict() for todo in self.todos], f, indent=2)

    def load_todos(self):
        """Load todos from the storage file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.todos = [TodoItem.from_dict(item) for item in data]
                    self._update_next_id()
            except (json.JSONDecodeError, KeyError):
                self.todos = []
                self.next_id = 1


def print_menu():
    """Print the main menu"""
    print("\n" + "="*50)
    print("           TODO APPLICATION")
    print("="*50)
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Update Task")
    print("4. Complete Task")
    print("5. Delete Task")
    print("6. Show Task Details")
    print("7. Help")
    print("8. Exit")
    print("="*50)


def print_help():
    """Print help information"""
    print("\nCOMMAND REFERENCE:")
    print("Add Task: Add a new task with title, description, priority, category, due date, and recurring pattern")
    print("List Tasks: View all tasks or filter by status/priority")
    print("Update Task: Modify an existing task's details")
    print("Complete Task: Mark a task as completed")
    print("Delete Task: Remove a task permanently")
    print("Show Task Details: View detailed information about a specific task")
    print("Help: Show this help message")
    print("Exit: Quit the application")


def main():
    """Main function to run the Todo application"""
    print("Welcome to the Advanced Todo App!")
    print("Type '7' or 'help' for available commands.")
    
    todo_manager = TodoManager()
    
    while True:
        print_menu()
        try:
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == "1" or choice.lower() == "add":
                print("\n--- ADD TASK ---")
                title = input("Enter task title: ").strip()
                if not title:
                    print("Title is required!")
                    continue
                
                description = input("Enter description (optional): ").strip()
                priority_input = input("Enter priority (High/Medium/Low, default: Medium): ").strip()
                priority = priority_input if priority_input in ["High", "Medium", "Low"] else "Medium"
                
                category = input("Enter category (optional): ").strip()
                due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
                
                recurring_input = input("Enter recurring pattern (Daily/Weekly/Monthly, optional): ").strip()
                recurring_pattern = recurring_input if recurring_input in ["Daily", "Weekly", "Monthly"] else ""
                
                todo = todo_manager.add_todo(title, description, priority, category, due_date, recurring_pattern)
                if todo:
                    print(f"Task added successfully with ID: {todo.id}")
                
            elif choice == "2" or choice.lower() == "list":
                print("\n--- LIST TASKS ---")
                print("1. All Tasks")
                print("2. Pending Tasks Only")
                print("3. Sort by Priority")
                
                list_choice = input("Choose option (1-3): ").strip()
                
                show_completed = True
                sort_by_priority = False
                
                if list_choice == "2":
                    show_completed = False
                elif list_choice == "3":
                    sort_by_priority = True
                
                todos = todo_manager.list_todos(show_completed, sort_by_priority)
                
                if not todos:
                    print("No tasks found.")
                else:
                    print(f"\n{'ID':<3} {'Status':<6} {'Priority':<8} {'Title':<20} {'Category':<12} {'Due Date':<12} {'Recurring':<10}")
                    print("-" * 90)
                    for todo in todos:
                        status = "✓" if todo.completed else "○"
                        category = todo.category if todo.category else "N/A"
                        due_date = todo.due_date if todo.due_date else "N/A"
                        recurring = todo.recurring_pattern if todo.recurring_pattern else "N/A"
                        print(f"{todo.id:<3} {status:<6} {todo.priority:<8} {todo.title[:19]:<20} {category[:11]:<12} {due_date:<12} {recurring:<10}")
                        
            elif choice == "3" or choice.lower() == "update":
                print("\n--- UPDATE TASK ---")
                try:
                    task_id = int(input("Enter task ID to update: "))
                    todo = todo_manager.get_todo(task_id)
                    if not todo:
                        print(f"Task with ID {task_id} not found.")
                        continue
                    
                    print(f"Current task: {todo}")
                    print("Leave blank to keep current value")
                    
                    new_title = input(f"Enter new title (current: {todo.title}): ").strip()
                    new_description = input(f"Enter new description (current: {todo.description}): ").strip()
                    new_priority = input(f"Enter new priority (High/Medium/Low, current: {todo.priority}): ").strip()
                    new_category = input(f"Enter new category (current: {todo.category}): ").strip()
                    new_due_date = input(f"Enter new due date (YYYY-MM-DD, current: {todo.due_date}): ").strip()
                    new_recurring = input(f"Enter new recurring pattern (Daily/Weekly/Monthly, current: {todo.recurring_pattern}): ").strip()
                    
                    # Process updates (use current value if input is empty)
                    title = new_title if new_title else None
                    description = new_description if new_description else None
                    priority = new_priority if new_priority in ["High", "Medium", "Low"] else None
                    category = new_category if new_category else None
                    due_date = new_due_date if new_due_date else None
                    recurring_pattern = new_recurring if new_recurring in ["Daily", "Weekly", "Monthly"] else None
                    
                    if todo_manager.update_todo(task_id, title, description, priority, category, due_date, recurring_pattern):
                        print("Task updated successfully!")
                    else:
                        print("Failed to update task.")
                        
                except ValueError:
                    print("Task ID must be a number.")
                
            elif choice == "4" or choice.lower() == "complete":
                print("\n--- COMPLETE TASK ---")
                try:
                    task_id = int(input("Enter task ID to mark as complete: "))
                    if todo_manager.toggle_completion(task_id):
                        todo = todo_manager.get_todo(task_id)
                        status = "completed" if todo.completed else "incomplete"
                        print(f"Task marked as {status}.")
                        
                        # If it was a recurring task, inform about the new task created
                        if todo.recurring_pattern and todo.completed:
                            print(f"New recurring task created based on pattern: {todo.recurring_pattern}")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError:
                    print("Task ID must be a number.")
                
            elif choice == "5" or choice.lower() == "delete":
                print("\n--- DELETE TASK ---")
                try:
                    task_id = int(input("Enter task ID to delete: "))
                    if todo_manager.remove_todo(task_id):
                        print("Task deleted successfully.")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError:
                    print("Task ID must be a number.")
                
            elif choice == "6" or choice.lower() == "show":
                print("\n--- TASK DETAILS ---")
                try:
                    task_id = int(input("Enter task ID to view: "))
                    todo = todo_manager.get_todo(task_id)
                    if todo:
                        print(f"\nID: {todo.id}")
                        print(f"Title: {todo.title}")
                        print(f"Description: {todo.description}")
                        print(f"Status: {'Completed' if todo.completed else 'Pending'}")
                        print(f"Priority: {todo.priority}")
                        print(f"Category: {todo.category if todo.category else 'None'}")
                        print(f"Due Date: {todo.due_date if todo.due_date else 'None'}")
                        print(f"Recurring: {todo.recurring_pattern if todo.recurring_pattern else 'No'}")
                        print(f"Created: {todo.created_at}")
                        print(f"Updated: {todo.updated_at}")
                    else:
                        print(f"Task with ID {task_id} not found.")
                except ValueError:
                    print("Task ID must be a number.")
                
            elif choice == "7" or choice.lower() == "help":
                print_help()
                
            elif choice == "8" or choice.lower() in ["exit", "quit"]:
                print("Thank you for using the Advanced Todo App!")
                break
                
            else:
                print("Invalid choice. Please enter a number between 1-8.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()