import uuid
from datetime import datetime
from config import table

def add_task(task_name, due_date=None):
    task_id = str(uuid.uuid4())
    item = {
        "task_id": task_id,
        "task_name": task_name,
        "completed": False,
    }
    if due_date:
        item["due_date"] = due_date
    table.put_item(Item=item)

def mark_task_completed(task_id):
    response = table.update_item(
        Key={"task_id": task_id},
        UpdateExpression="set completed = :val",
        ExpressionAttributeValues={":val": True},
        ReturnValues="UPDATED_NEW"
    )
    return response

from datetime import datetime

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

        print(f"{task_id} - {task_name} [{status}] - Due: {due}{overdue}")



def edit_task_name(task_id, new_name, new_due=None):
    update_expr = "set task_name = :name"
    expr_values = {":name": new_name}
    if new_due:
        update_expr += ", due_date = :due"
        expr_values[":due"] = new_due
    response = table.update_item(
        Key={"task_id": task_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values,
        ReturnValues="UPDATED_NEW"
    )
    return response


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
