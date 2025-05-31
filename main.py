from dynamo_handler import (
    add_task,
    list_tasks,
    mark_task_completed,
    edit_task,
    delete_task,
    list_completed_tasks,
    list_pending_tasks,
    list_overdue_tasks,
    delete_completed_tasks,
    export_tasks_to_csv,
    filter_tasks_by_priority,
    filter_tasks_by_tag,
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
        print("8. View overdue tasks")
        print("9. Delete all completed tasks")
        print("10. Export tasks to CSV")
        print("11. View tasks by priority")
        print("12. View tasks by tag")
        print("15. Exit")


        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter task: ")
            due_date = input("Enter due date (YYYY-MM-DD) [optional]: ")
            priority = input("Enter priority (High/Medium/Low) [default: Medium]: ").capitalize()
            if priority not in ["High", "Medium", "Low"]:
                priority = "Medium"
            tags_input = input("Enter tags (comma-separated) [optional]: ")
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            add_task(task, due_date, priority, tags)

        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = input("Enter Task ID to mark as completed: ")
            mark_task_completed(task_id)
            print("Task marked as completed.")
        elif choice == "4":
            task_id = input("Enter task ID to edit: ")
            new_name = input("Enter new task name (leave blank to keep unchanged): ")
            new_due = input("Enter new due date (YYYY-MM-DD) [leave blank to keep unchanged]: ")
            new_name = new_name if new_name.strip() else None
            new_due = new_due if new_due.strip() else None
            edit_task(task_id, new_name, new_due)
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
            list_overdue_tasks()
        elif choice == "9":
            delete_completed_tasks()
        elif choice == "10":
            filename = input("Enter filename [default: tasks_export.csv]: ").strip()
            if not filename:
                filename = "tasks_export.csv"
            export_tasks_to_csv(filename)  
        elif choice == "11":
            priority = input("Enter priority to filter by (High/Medium/Low): ").capitalize()
            if priority not in ["High", "Medium", "Low"]:
                print("Invalid priority.")
            else:
                filter_tasks_by_priority(priority)
        elif choice == "12":
            tag = input("Enter tag to filter by: ").strip()
            if not tag:
                print("Tag cannot be empty.")
            else:
                filter_tasks_by_tag(tag)
        elif choice == "15":
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()
