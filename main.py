from dynamo_handler import add_task, list_tasks, mark_task_completed


def menu():
    while True:
        print("\nTO-DO LIST MENU")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Completed")  # 👈 NEW
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter task: ")
            add_task(task)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = input("Enter Task ID to mark as completed: ")
            mark_task_completed(task_id)
        elif choice == "4":
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()
