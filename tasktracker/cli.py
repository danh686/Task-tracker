import typer
import os
from pathlib import Path
from . import main
from . import utils


app = typer.Typer()


@app.command()
def add(
    file: Path = typer.Option(
        default="tasks.csv", help="The csv file which stores the tasks"
    )
):
    """
    Add a task
    """
    if os.path.exists(file):
        tasks = main.FileHandler.load(file)
    else:
        tasks = main.Tasks()
    id = utils.get_new_id(tasks)
    summary = input("Summary: ")
    description = input("Description (optional): ")
    due_date = utils.get_date()
    status = utils.get_status()
    tasks.add(id, summary, description, due_date, status)
    main.FileHandler.save(file, tasks)
    print("Task added successfully")

@app.command()
def show(
    file: Path = typer.Option(
        default="tasks.csv", help="The csv file which stores the tasks"
    )
):
    """
    Show a grid layout of the tasks
    """
    if not os.path.exists(file):
        raise Exception("Error: tasks file not found")
    main.FileHandler.show(file)


@app.command()
def update(
    file: Path = typer.Option(
        default="tasks.csv", help="The csv file which stores the tasks"
    )
):
    """
    Update a task
    """
    if not os.path.exists(file):
        raise FileNotFoundError("Error: tasks file not found")

    main.FileHandler.show(file)
    tasks = main.FileHandler.load(file)
    id = input("Enter the ID of the task to update: ")
    task_to_update = new_task = tasks.find(id)
    if not task_to_update:
        raise Exception(f"Error: task with ID of {id} does not exist")

    field_to_update = input(
        "Enter the field to update\n1: Summary\n2: Description\n3: Status\n4: Due date\n"
    )

    match field_to_update:
        case "1":
            new_task.summary = input("Summary: ")
        case "2":
            new_task.description = input(f"Description (optional): ")
        case "3":
            new_task.status = utils.get_status()
        case "4":
            new_task.due_date = utils.get_date()
        case _:
            raise Exception("Error: invalid input")
    tasks.update(task_to_update, new_task)
    main.FileHandler.save(file, tasks)
    print("Task updated successfully")


@app.command()
def delete(
    file: Path = typer.Option(
        default="tasks.csv", help="The csv file which stores the tasks"
    ),
):
    """
    Delete a task
    """
    if not os.path.exists(file):
        raise FileNotFoundError("Error: tasks file not found")
    main.FileHandler.show(file)
    tasks = main.FileHandler.load(file)
    id = input("Enter the ID of the task to delete: ")
    task_to_delete = tasks.find(id)
    if not task_to_delete:
        raise Exception(f"Error: task with ID of {id} does not exist")
    tasks.delete(task_to_delete)
    main.FileHandler.save(file, tasks)
    print("Task deleted successfully")

def script():
    app()
