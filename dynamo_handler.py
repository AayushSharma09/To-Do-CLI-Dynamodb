import uuid
from config import table

def add_task(task_name):
    task_id = str(uuid.uuid4())
    table.put_item(
        Item={
            "task_id": task_id,
            "task_name": task_name,
            "completed": False   # 👈 NEW FIELD
        }
    )
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

    for task in tasks:
        status = "✅" if task.get("completed") else "⏳"
        print(f"{task['task_id']} - {task['task_name']} [{status}]")

def delete_task(task_id):
    table.delete_item(Key={"task_id": task_id})
    print(f"Deleted task with ID: {task_id}")
