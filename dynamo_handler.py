import uuid
from config import table

def add_task(task_name):
    task_id = str(uuid.uuid4())
    table.put_item(Item={"task_id": task_id, "task_name": task_name})
    print(f"Task added: {task_name} (ID: {task_id})")

def list_tasks():
    response = table.scan()
    tasks = response.get('Items', [])
    for task in tasks:
        print(f"{task['task_id']}: {task['task_name']}")

def delete_task(task_id):
    table.delete_item(Key={"task_id": task_id})
    print(f"Deleted task with ID: {task_id}")
