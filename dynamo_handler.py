import uuid
from datetime import datetime
from config import table

def add_task(task_name, due_date=None, priority="Medium"):
    task_id = str(uuid.uuid4())[:8]
    item = {
        "task_id": task_id,
        "task_name": task_name,
        "completed": False,
        "priority": priority
    }

    if due_date:
        item["due_date"] = due_date

    table.put_item(Item=item)
    print("Task added successfully.")

def mark_task_completed(task_id):
    response = table.update_item(
        Key={"task_id": task_id},
        UpdateExpression="set completed = :val",
        ExpressionAttributeValues={":val": True},
        ReturnValues="UPDATED_NEW"
    )
    return response
    
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

