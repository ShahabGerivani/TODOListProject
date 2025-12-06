from typing import cast
from datetime import datetime

from src.TODOListProject.db import DBInterface
from src.TODOListProject.model.models import Project, TaskStatus, Task


class ProjectTaskController:
    """Controller class for communication between user interface and database"""

    def __init__(self, db: DBInterface):
        self.__db = db

    def create_project(self, name: str, description: str = "") -> None:
        """
        Create a new project with given name and description.
        :param name:
        :param description:
        :return:
        :raise DBFullError: If maximum number of projects is reached in the database.
        """
        self.__db.update_or_insert(
            "projects",
            Project(self.__db.get_next_id("projects"), name, description)
        )

    def edit_project(self, project_id: int, name: str | None = None, description: str | None = None) -> None:
        """
        Edit an existing project with given ID. If name and description are not None, the project will be updated.
        :param project_id:
        :param name:
        :param description:
        :return:
        :raise KeyError: If not found
        """
        project = cast(Project, self.__db.get_by_id("projects", project_id))
        new_project = Project(project_id, project.name, project.description)
        if name is not None:
            new_project.name = name
        if description is not None:
            new_project.description = description
        self.__db.update_or_insert("projects", new_project)

    def delete_project(self, project_id: int) -> None:
        """
        Delete an existing project with given ID.
        :param project_id:
        :return:
        :raise KeyError: If not found
        """
        self.__db.delete("projects", project_id)

    def get_all_projects(self) -> list[Project]:
        return self.__db.get_all("projects")

    def create_task(self, project_id: int, name: str, description: str = "", status: TaskStatus = TaskStatus.todo,
                    deadline: datetime = None) -> None:
        """
        Create a new task. only project_id and name are required.
        :param project_id:
        :param name:
        :param description:
        :param status:
        :param deadline:
        :return:
        :raise DBFullError: If maximum number of tasks is reached.
        :raise KeyError: If project not found
        :raises ValueError: If deadline is in the past
        """
        if deadline is not None and deadline < datetime.now():
            raise ValueError("Deadline must be in the future")
        self.__db.update_or_insert(
            "tasks",
            Task(self.__db.get_next_id("tasks"), project_id, name, description, status, deadline)
        )

    def edit_task(self, task_id: int, name: str = None, description: str = None, status: TaskStatus = None,
                  deadline: datetime = None) -> None:
        """
        Edit task with given ID. For each task property, if anything other than None is given, it will be updated.
        :param task_id:
        :param name:
        :param description:
        :param status:
        :param deadline:
        :return:
        :raise KeyError: If not found
        :raises ValueError: If deadline is in the past
        """
        task = cast(Task, self.__db.get_by_id("tasks", task_id))
        new_task = Task(task_id, task.project_id, task.name, task.description, task.status, task.deadline)
        if name is not None:
            new_task.name = name
        if description is not None:
            new_task.description = description
        if status is not None:
            new_task.status = status
        if deadline is not None:
            if deadline < datetime.now():
                raise ValueError("Deadline must be in the future")
            new_task.deadline = deadline
        self.__db.update_or_insert("tasks", new_task)

    def delete_task(self, task_id: int) -> None:
        """
        Delete task with given ID.
        :param task_id:
        :return:
        :raise KeyError: If not found
        """
        self.__db.delete("tasks", task_id)

    def get_all_tasks(self, project_id: int) -> list[Task]:
        return list(cast(Project, self.__db.get_by_id("projects", project_id)).tasks.values())
