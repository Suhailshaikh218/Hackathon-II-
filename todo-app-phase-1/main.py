from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single task in the todo list."""
    id: int
    title: str
    description: str
    status: str  # 'pending' or 'completed'
    created_at: datetime

    def __str__(self) -> str:
        """String representation of a task."""
        return f"Task {self.id}: [{self.status}] {self.title} - {self.description} (Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"


class TodoCore:
    """Core todo application with in-memory storage."""

    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task with title and optional description. Returns the created task."""
        if not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            status='pending',
            created_at=datetime.now()
        )
        self.tasks.append(task)
        task_id = self.next_id
        self.next_id += 1

        # Return a copy to prevent external modification
        return Task(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at
        )

    def view_all_tasks(self) -> List[Task]:
        """Return all tasks sorted by creation date (newest first)."""
        # Sort tasks by creation date (newest first)
        sorted_tasks = sorted(self.tasks, key=lambda t: t.created_at, reverse=True)

        # Return copies to prevent external modification
        return [
            Task(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                created_at=task.created_at
            )
            for task in sorted_tasks
        ]

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update a task's title and/or description. Returns the updated task or None if not found."""
        for task in self.tasks:
            if task.id == task_id:
                if title is not None:
                    task.title = title.strip() if title.strip() else task.title
                if description is not None:
                    task.description = description.strip()

                # Return a copy to prevent external modification
                return Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    status=task.status,
                    created_at=task.created_at
                )

        return None

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID. Returns True if successful."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def mark_task_completed(self, task_id: int) -> bool:
        """Mark a task as completed by its ID. Returns True if successful."""
        for task in self.tasks:
            if task.id == task_id:
                task.status = 'completed'
                return True
        return False


def display_menu():
    """Display the main menu options."""
    print("\n" + "="*40)
    print("           TODO APP - MAIN MENU")
    print("="*40)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task as Completed")
    print("6. Exit")
    print("="*40)


def get_user_choice() -> str:
    """Get and validate user's menu choice."""
    while True:
        choice = input("Enter your choice (1-6): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice
        print("Invalid choice. Please enter a number between 1 and 6.")


def handle_add_task(app: TodoCore):
    """Handle adding a new task."""
    print("\n--- Add New Task ---")
    title = input("Enter task title: ").strip()
    if not title:
        print("❌ Task title cannot be empty.")
        return

    description = input("Enter task description (optional): ").strip()

    try:
        task = app.add_task(title, description)
        print(f"✅ Task added successfully!")
        print(f"   ID: {task.id}")
        print(f"   Title: {task.title}")
        print(f"   Description: {task.description if task.description else '(No description)'}")
    except ValueError as e:
        print(f"❌ Error: {e}")


def handle_view_tasks(app: TodoCore):
    """Handle viewing all tasks."""
    print("\n--- All Tasks ---")
    tasks = app.view_all_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status_icon = "✅" if task.status == 'completed' else "⏳"
        print(f"\n{status_icon} ID: {task.id}")
        print(f"   Title: {task.title}")
        print(f"   Description: {task.description if task.description else '(No description)'}")
        print(f"   Status: {task.status}")
        print(f"   Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")


def handle_update_task(app: TodoCore):
    """Handle updating a task."""
    print("\n--- Update Task ---")
    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("❌ Please enter a valid task ID (number).")
        return

    # Check if task exists
    task_exists = any(task.id == task_id for task in app.view_all_tasks())
    if not task_exists:
        print(f"❌ Task with ID {task_id} not found.")
        return

    print("Leave blank to keep current value.")
    new_title = input("Enter new title (or press Enter to keep current): ").strip()
    new_description = input("Enter new description (or press Enter to keep current): ").strip()

    # Prepare update parameters
    title_update = new_title if new_title else None
    description_update = new_description if new_description else None

    # If both are None, no update needed
    if title_update is None and description_update is None:
        print("No changes made.")
        return

    updated_task = app.update_task(task_id, title_update, description_update)

    if updated_task:
        print(f"✅ Task {task_id} updated successfully!")
        print(f"   New Title: {updated_task.title}")
        print(f"   New Description: {updated_task.description if updated_task.description else '(No description)'}")
    else:
        print(f"❌ Failed to update task with ID {task_id}.")


def handle_delete_task(app: TodoCore):
    """Handle deleting a task."""
    print("\n--- Delete Task ---")
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("❌ Please enter a valid task ID (number).")
        return

    confirm = input(f"Are you sure you want to delete task {task_id}? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y"]:
        print("❌ Deletion cancelled.")
        return

    if app.delete_task(task_id):
        print(f"✅ Task {task_id} deleted successfully!")
    else:
        print(f"❌ Task with ID {task_id} not found.")


def handle_mark_completed(app: TodoCore):
    """Handle marking a task as completed."""
    print("\n--- Mark Task as Completed ---")
    try:
        task_id = int(input("Enter task ID to mark as completed: "))
    except ValueError:
        print("❌ Please enter a valid task ID (number).")
        return

    # Check if task exists
    task_exists = any(task.id == task_id for task in app.view_all_tasks())
    if not task_exists:
        print(f"❌ Task with ID {task_id} not found.")
        return

    if app.mark_task_completed(task_id):
        print(f"✅ Task {task_id} marked as completed!")
    else:
        print(f"❌ Failed to mark task {task_id} as completed.")


def main():
    """Main function to run the todo app."""
    app = TodoCore()

    print("🎯 Welcome to the Todo App!")
    print("Manage your tasks efficiently with this simple tool.")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            handle_add_task(app)
        elif choice == "2":
            handle_view_tasks(app)
        elif choice == "3":
            handle_update_task(app)
        elif choice == "4":
            handle_delete_task(app)
        elif choice == "5":
            handle_mark_completed(app)
        elif choice == "6":
            print("\n👋 Thank you for using the Todo App! Goodbye!")
            break

        # Pause to let user see the result before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
