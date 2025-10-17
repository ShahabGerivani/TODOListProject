from typing import cast
from datetime import datetime

from src.TODOListProject.db import DBInterface
from src.TODOListProject.models import Project, TaskStatus, Task


class ProjectTaskController:
    def __init__(self, db: DBInterface):
        self.__db = db

    def create_project(self, name: str, description: str = "") -> None:
        self.__db.update_or_insert(
            "projects",
            Project(self.__db.get_next_id("projects"), name, description)
        )

    def edit_project(self, project_id: int, name: str = None, description: str = None) -> None:
        project = cast(Project, self.__db.get_by_id("projects", project_id))
        new_project = Project(project_id, project.name, project.description)
        if name is not None:
            new_project.name = name
        if description is not None:
            new_project.description = description
        self.__db.update_or_insert("projects", new_project)

    def delete_project(self, project_id: int) -> None:
        self.__db.delete("projects", project_id)

    def get_all_projects(self) -> list[Project]:
        return self.__db.get_all("projects")

    def create_task(self, project_id: int, name: str, description: str = "", status: TaskStatus = TaskStatus.todo,
                    deadline: datetime = None) -> None:
        self.__db.update_or_insert(
            "tasks",
            Task(self.__db.get_next_id("tasks"), project_id, name, description, status, deadline)
        )

    def edit_task(self, task_id: int, name: str = None, description: str = None, status: TaskStatus = None, deadline: datetime = None) -> None:
        task = cast(Task, self.__db.get_by_id("tasks", task_id))
        new_task = Task(task_id, task.project_id, task.name, task.description, task.status, task.deadline)
        if name is not None:
            new_task.name = name
        if description is not None:
            new_task.description = description
        if status is not None:
            new_task.status = status
        if deadline is not None:
            new_task.deadline = deadline
        self.__db.update_or_insert("tasks", new_task)

    def delete_task(self, task_id: int) -> None:
        self.__db.delete("tasks", task_id)

    def get_all_tasks(self, project_id: int) -> list[Task]:
        return cast(Project, self.__db.get_by_id("projects", project_id)).tasks.values()
