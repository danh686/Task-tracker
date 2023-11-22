import csv
from dataclasses import dataclass
from tabulate import tabulate
from pathlib import Path
from . import utils


class Tasks:
    def __init__(self):
        self.tasks = []

    def add(self, id: str, summary: str, description: str, due_date: str, status: str):
        task = Task(id, summary, description, status, due_date)
        self.tasks.append(task)

    def update(self, task_to_update, updated_task):
        for i, task in enumerate(self.tasks):
            if task == task_to_update:
                self.tasks[i] = updated_task

    def delete(self, task):
        self.tasks.remove(task)

    def find(self, id):
        for task in self.tasks:
            if task.id == id:
                return task


@dataclass
class Task:
    id: str
    summary: int
    description: str
    status: str
    due_date: str


class FileHandler:
    @staticmethod
    def load(path: Path) -> Tasks:
        """
        Read tasks from a file and return them as Task objects
        """
        with path.open() as file:
            reader = csv.DictReader(file)
            tasks = Tasks()
            for row in reader:
                tasks.tasks.append(
                    Task(
                        row["ID"],
                        row["Summary"],
                        row["Description"],
                        row["Status"],
                        row["Due date"],
                    )
                )
            return tasks

    @staticmethod
    def save(path: Path, tasks: Tasks):
        """
        Take a Tasks object as input and write the tasks to a file
        """
        with path.open(mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Summary", "Description", "Status", "Due date"])
            for task in tasks.tasks:
                writer.writerow(
                    [
                        task.id,
                        task.summary,
                        task.description,
                        task.status,
                        task.due_date,
                    ]
                )

    @staticmethod
    def show(path: Path):
        """
        Show the tasks in a grid layout
        """
        data = []
        with path.open() as file:
            reader = csv.reader(file)
            for row in reader:
                row[1] = utils.format_string(row[1], max_length=30)
                row[2] = utils.format_string(row[2], max_length=75)
                data.append(row)
        print(tabulate(data[1:], data[0], tablefmt="grid"))
