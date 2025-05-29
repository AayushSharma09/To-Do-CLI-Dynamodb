from dynamo_handler import (
    add_task,
    list_tasks,
    mark_task_completed,
    edit_task_name,
    delete_task,
    list_completed_tasks,
    list_pending_tasks
)

def menu():
    while True:
        print("\nTO-DO LIST MENU")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Completed")  # 👈 NEW
        print("4. Edit Task")
        print("5. Delete Task") 
        print("6. Show Completed Tasks")    # 👈 NEW
        print("7. Show Pending Tasks")      # 👈 NEW
        print("8. Exit")


        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter task: ")
            due_date = input("Enter due date (YYYY-MM-DD) [optional]: ")
            due_date = due_date if due_date.strip() else None
            add_task(task, due_date)
            print("Task added successfully.")
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = input("Enter Task ID to mark as completed: ")
            mark_task_completed(task_id)
            print("Task marked as completed.")
        elif choice == "4":
            task_id = input("Enter Task ID to edit: ")
            new_name = input("Enter new task name: ")
            new_due = input("Enter new due date (YYYY-MM-DD) [optional]: ")
            new_due = new_due if new_due.strip() else None
            edit_task_name(task_id, new_name, new_due)
            print("Task updated successfully.")
        elif choice == "5":
            task_id = input("Enter task ID to delete: ")
            delete_task(task_id)
            print("Task deleted successfully.")
        elif choice == "6":
            list_completed_tasks()
        elif choice == "7":
            list_pending_tasks()
        elif choice == "8":
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()
