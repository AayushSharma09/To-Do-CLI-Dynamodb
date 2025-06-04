import uuid
import csv
from datetime import datetime, date
from config import table
from datetime import timedelta

def add_task(task_name, due_date=None, priority=None, recurrence="none", tags=None):
    task_id = str(uuid.uuid4())
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = {
        "task_id": task_id,
        "task_name": task_name,
        "created_at": created_at,
        "completed": False,
        "recurrence": recurrence,
        "priority": priority or "normal",
    }
    if due_date:
        item["due_date"] = due_date
    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        item["tags"] = tag_list
    table.put_item(Item=item)
    print("Task added successfully.")


def mark_task_completed(task_id):
    response = table.get_item(Key={"task_id": task_id})
    task = response.get("Item")

    if not task:
        print("Task not found.")
        return

    table.update_item(
        Key={"task_id": task_id},
        UpdateExpression="SET completed = :val",
        ExpressionAttributeValues={":val": True}
    )
    print("Task marked as completed.")

    recurrence = task.get("recurrence", "none")
    if recurrence != "none":
        new_due_date = task.get("due_date")
        if new_due_date:
            try:
                current_due = datetime.strptime(new_due_date, "%Y-%m-%d")
                if recurrence == "daily":
                    new_due = current_due + timedelta(days=1)
                elif recurrence == "weekly":
                    new_due = current_due + timedelta(weeks=1)
                elif recurrence == "monthly":
                    new_due = current_due.replace(month=current_due.month % 12 + 1)
                new_due_str = new_due.strftime("%Y-%m-%d")
            except:
                new_due_str = None
        else:
            new_due_str = None

        add_task(
            task_name=task["task_name"],
            due_date=new_due_str,
            priority=task.get("priority", "Medium"),
            tags=task.get("tags", []),
            recurrence=recurrence
        )
    
def list_tasks():
    response = table.scan()
    tasks = response.get("Items", [])
    if not tasks:
        print("No tasks found.")
        return

    today = datetime.today().date()

    for task in tasks:
        task_id = task.get("task_id", "N/A")
        task_name = task.get("task_name", "[Unnamed Task]")
        completed = task.get("completed", False)
        status = "✅" if completed else "⏳"
        due = task.get("due_date", None)
        overdue = ""

        if due:
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
                if not completed and due_date < today:
                    overdue = " ⚠️ OVERDUE"
            except Exception as e:
                due = f"Invalid Date"

        else:
            due = "No Due Date"
        priority = task.get("priority", "Medium")
        print(f"{task_id} - {task_name} [{status}] - Due: {due}{overdue} - Priority: {priority}")
        tags = ", ".join(task.get("tags", []))
        if tags:
            print(f"   Tags: {tags}")

def edit_task(task_id, new_name=None, new_due_date=None):
    update_expression = []
    expression_values = {}

    if new_name:
        update_expression.append("task_name = :n")
        expression_values[":n"] = new_name
    if new_due_date:
        update_expression.append("due_date = :d")
        expression_values[":d"] = new_due_date
    if not update_expression:
        print("Nothing to update.")
        return

    table.update_item(
        Key={"task_id": task_id},
        UpdateExpression="SET " + ", ".join(update_expression),
        ExpressionAttributeValues=expression_values
    )
    print("Task updated successfully.")


def delete_task(task_id):
    table.delete_item(Key={"task_id": task_id})
    print(f"Deleted task with ID: {task_id}")

# newer
def list_completed_tasks():
    response = table.scan(
        FilterExpression="completed = :val",
        ExpressionAttributeValues={":val": True}
    )
    tasks = response.get("Items", [])
    today = datetime.today().date()

    for task in tasks:
        task_id = task.get("task_id", "N/A")
        task_name = task.get("task_name", "[Unnamed Task]")
        status = "✅" if task.get("completed") else "⏳"
        due = task.get("due_date")
        overdue = ""

        if due:
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
                if not task.get("completed") and due_date < today:
                    overdue = " ⚠️ OVERDUE"
            except ValueError:
                due = "Invalid Date Format"
        else:
            due = "No Due Date"

        print(f"{task_id} - {task_name} [{status}] - Due: {due}{overdue}")

def list_pending_tasks():
    response = table.scan(
        FilterExpression="completed = :val",
        ExpressionAttributeValues={":val": False}
    )
    tasks = response.get("Items", [])
    today = datetime.today().date()

    for task in tasks:
        task_id = task.get("task_id", "N/A")
        task_name = task.get("task_name", "[Unnamed Task]")
        status = "✅" if task.get("completed") else "⏳"
        due = task.get("due_date")
        overdue = ""

        if due:
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
                if not task.get("completed") and due_date < today:
                    overdue = " ⚠️ OVERDUE"
            except ValueError:
                due = "Invalid Date Format"
        else:
            due = "No Due Date"

        print(f"{task_id} - {task_name} [{status}] - Due: {due}{overdue}")

def list_overdue_tasks():
    response = table.scan()
    tasks = response.get("Items", [])
    if not tasks:
        print("No tasks found.")
        return

    today = datetime.today().date()
    overdue_found = False

    for task in tasks:
        task_name = task.get("task_name", "[Unnamed Task]")
        completed = task.get("completed", False)
        due = task.get("due_date")

        if due and not completed:
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
                if due_date < today:
                    print(f"{task['task_id']} - {task_name} ⏳ - Due: {due} ⚠️ OVERDUE")
                    overdue_found = True
            except:
                continue

    if not overdue_found:
        print("No overdue tasks found.")

def delete_completed_tasks():
    response = table.scan()
    tasks = response.get("Items", [])

    if not tasks:
        print("No tasks found.")
        return

    deleted = 0
    for task in tasks:
        if task.get("completed"):
            table.delete_item(Key={"task_id": task["task_id"]})
            deleted += 1

    if deleted:
        print(f"Deleted {deleted} completed task(s).")
    else:
        print("No completed tasks to delete.")

def export_tasks_to_csv(filename="tasks_export.csv"):
    response = table.scan()
    tasks = response.get("Items", [])

    if not tasks:
        print("No tasks to export.")
        return

    with open(filename, mode="w", newline="") as csv_file:
        fieldnames = ["task_id", "task_name", "completed", "due_date", "priority"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for task in tasks:
            writer.writerow({
                "task_id": task.get("task_id", ""),
                "task_name": task.get("task_name", ""),
                "completed": task.get("completed", False),
                "due_date": task.get("due_date", ""),
                "priority": task.get("priority", "Medium")
            })

    print(f"Tasks exported successfully to {filename}.")

def filter_tasks_by_priority(priority_level):
    response = table.scan()
    tasks = response.get("Items", [])

    filtered = [task for task in tasks if task.get("priority", "Medium").lower() == priority_level.lower()]

    if not filtered:
        print(f"No {priority_level} priority tasks found.")
        return

    print(f"\n{priority_level.upper()} PRIORITY TASKS:")
    for task in filtered:
        task_id = task["task_id"]
        task_name = task["task_name"]
        status = "✅" if task.get("completed") else "⏳"
        due = task.get("due_date", "N/A")
        print(f"{task_id} - {task_name} [{status}] - Due: {due}")

def filter_tasks_by_tags(tag_input):
    input_tags = set(tag.strip().lower() for tag in tag_input.split(","))
    response = table.scan()
    tasks = response.get("Items", [])
    filtered = []

    for task in tasks:
        task_tags = set(task.get("tags", []))
        if input_tags & task_tags:  # intersection means at least one tag matches
            filtered.append(task)

    if not filtered:
        print("No tasks match the specified tags.")
        return

    print("\nTasks matching tags:")
    for task in filtered:
        status = "✅" if task.get("completed") else "⏳"
        tags = ", ".join(task.get("tags", []))
        print(f"{task['task_id']} - {task['task_name']} [{status}] Tags: {tags}")


def list_tasks_sorted_by_due_date():
    response = table.scan()
    tasks = response.get("Items", [])

    def parse_due_date(task):
        due_str = task.get("due_date")
        try:
            return datetime.strptime(due_str, "%Y-%m-%d") if due_str else datetime.max
        except:
            return datetime.max

    sorted_tasks = sorted(tasks, key=parse_due_date)

    if not sorted_tasks:
        print("No tasks found.")
        return

    print("\nTASKS SORTED BY DUE DATE:")
    for task in sorted_tasks:
        task_id = task["task_id"]
        task_name = task["task_name"]
        status = "✅" if task.get("completed") else "⏳"
        due = task.get("due_date", "N/A")
        priority = task.get("priority", "Medium")
        tags = ", ".join(task.get("tags", []))
        overdue = ""
        if due != "N/A" and not task.get("completed"):
            try:
                due_date = datetime.strptime(due, "%Y-%m-%d").date()
                if due_date < date.today():
                    overdue = " (Overdue)"
            except ValueError:
                pass

        print(f"{task_id} - {task_name} [{status}] - Due: {due}{overdue} - Priority: {priority}")
        if tags:
            print(f"   Tags: {tags}")

def search_tasks(keyword):
    keyword = keyword.lower()
    response = table.scan()
    tasks = response.get("Items", [])

    found = False
    for task in tasks:
        name = task.get("task_name", "").lower()
        tags = [tag.lower() for tag in task.get("tags", [])]

        if keyword in name or keyword in tags:
            status = "✅" if task.get("completed") else "⏳"
            due_date = task.get("due_date", "N/A")
            print(f"{task['task_id']} - {task['task_name']} [{status}] - Due: {due_date}")
            found = True

    if not found:
        print("No matching tasks found.")

def daily_summary():
    response = table.scan()
    tasks = response.get("Items", [])

    total_tasks = len(tasks)
    completed = sum(1 for task in tasks if task.get("completed"))
    due_today = 0
    overdue = 0

    for task in tasks:
        due_date = task.get("due_date")
        if due_date:
            try:
                task_date = date.fromisoformat(due_date)
                if task_date == date.today():
                    due_today += 1
                elif task_date < date.today() and not task.get("completed"):
                    overdue += 1
            except ValueError:
                continue

    print("\n📊 DAILY SUMMARY")
    print(f"Total tasks: {total_tasks}")
    print(f"✅ Completed: {completed}")
    print(f"📅 Due today: {due_today}")
    print(f"⚠️ Overdue: {overdue}\n")

def list_tasks_due_today():
    today = date.today().isoformat()
    response = table.scan()
    tasks = response.get('Items', [])
    due_today = []

    for task in tasks:
        if task.get("due_date") == today and not task.get("completed", False):
            due_today.append(task)

    if due_today:
        print("\nTasks Due Today:")
        for task in due_today:
            print(f"{task['task_id']} - {task['task_name']} [⏰]")
    else:
        print("\nNo tasks due today.")
