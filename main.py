from dynamo_handler import add_task, list_tasks, delete_task

def menu():
    while True:
        print("\n-- To-Do List --")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Delete Task")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter task name: ")
            add_task(task)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = input("Enter task ID to delete: ")
            delete_task(task_id)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
