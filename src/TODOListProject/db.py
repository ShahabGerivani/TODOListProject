"""Database"""

from abc import ABC, abstractmethod
from typing import Any
import os
from typing import cast

from dotenv import load_dotenv

from src.TODOListProject.exceptions import DBFullError
from src.TODOListProject.models import NamedEntity, Project, Task


class DBInterface(ABC):
    """Abstract interface for DB interactions."""

    @abstractmethod
    def get_all(self, table: str) -> list:
        pass

    @abstractmethod
    def get_by_id(self, table: str, entity_id: int) -> object:
        pass

    @abstractmethod
    def update_or_insert(self, table: str, entity: object) -> None:
        pass

    @abstractmethod
    def delete(self, table: str, entity_id: int) -> None:
        pass

    @abstractmethod
    def get_next_id(self, table: str) -> int:
        pass


class InMemoryDB(DBInterface):
    """
    In memory DB interface.

    The projects and tasks are stored in dictionaries with their ID as key.

    IDs are kept track using __projects_next_id and __tasks_next_id.

    Maximum number of projects and tasks are loaded from .env file
    """

    def __init__(self):
        self.__projects: dict[int, Project] = {}
        self.__tasks: dict[int, Task] = {}
        self.__projects_next_id: int = 0
        self.__tasks_next_id: int = 0
        load_dotenv()
        self.__MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT"))
        self.__MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK"))

    def get_all(self, table: str) -> list[Any]:
        """
        Get all entities in table (projects/tasks).
        :param table: Either "projects" or "tasks"
        :return: The list of all Tasks or Projects
        :raise ValueError: If table is not "projects" or "tasks"
        """
        match table:
            case "projects":
                return list(self.__projects.values())
            case "tasks":
                return list(self.__tasks.values())
            case _:
                raise ValueError("Invalid table")

    def get_by_id(self, table: str, entity_id: int) -> object:
        """
        Get entity (Project/Task) by ID.
        :param table: Either "projects" or "tasks"
        :param entity_id: entity_id of project/task
        :return: The specified Project or Task
        :raise ValueError: If table is not "projects" or "tasks"
        :raise KeyError: If not found
        """
        match table:
            case "projects":
                return self.__projects[entity_id]
            case "tasks":
                return self.__tasks[entity_id]
            case _:
                raise ValueError("Invalid table")

    def update_or_insert(self, table: str, entity: NamedEntity) -> None:
        """
        Update/Insert entity (Project/Task) in database.
        :param table: Either "projects" or "tasks"
        :param entity: The Project or Task to update/insert. Update if the entities entity_id is already in the database. Insert otherwise.
        :return:
        :raise ValueError: If table is not "projects" or "tasks", or if project name is duplicated.
        :raise DBFullError: If maximum number of projects or tasks is reached.
        """
        match table:
            case "projects":
                # Checking for duplicate names
                for existing in self.__projects.values():
                    if existing.name == entity.name and existing.entity_id != entity.entity_id:
                        raise ValueError(f"Project with name '{entity.name}' already exists.")
                # -- Update --
                if entity.entity_id in self.__projects:
                    self.__projects[entity.entity_id] = cast(Project, entity)
                    return
                # -- Insert --
                if len(self.__projects) >= self.__MAX_NUMBER_OF_PROJECT:
                    raise DBFullError("Maximum number of projects reached")
                self.__projects[entity.entity_id] = cast(Project, entity)
                self.__projects_next_id += 1
            case "tasks":
                task = cast(Task, entity)
                project = cast(Project, self.__projects[task.project_id])
                # -- Update --
                if task.entity_id in self.__tasks:
                    self.__tasks[task.entity_id] = task
                    project.tasks[task.entity_id] = task
                    return
                # -- Insert --
                if len(self.__tasks) >= self.__MAX_NUMBER_OF_TASK:
                    raise DBFullError("Maximum number of tasks reached")
                self.__tasks[task.entity_id] = task
                project.tasks[task.entity_id] = task
                self.__tasks_next_id += 1
            case _:
                raise ValueError("Invalid table")

    def delete(self, table: str, entity_id: int) -> None:
        """
        Delete entity (Project/Task) by ID.
        :param table: Either "projects" or "tasks
        :param entity_id:
        :return:
        :raise ValueError: If table is not "projects" or "tasks"
        :raise KeyError: If not found
        """
        match table:
            case "projects":
                project = cast(Project, self.__projects[entity_id])
                for task in project.tasks.values():
                    del self.__tasks[task.entity_id]
                del self.__projects[entity_id]
            case "tasks":
                task = cast(Task, self.__tasks[entity_id])
                project = cast(Project, self.__projects[task.project_id])
                del project.tasks[task.entity_id]
                del self.__tasks[entity_id]
            case _:
                raise ValueError("Invalid table")

    def get_next_id(self, table: str) -> int:
        """
        Get next available ID for table (projects/tasks).
        :param table: Either "projects" or "tasks"
        :return: The next available ID in table (used for insertion)
        :raise ValueError: If table is not "projects" or "tasks"
        """
        match table:
            case "projects":
                return self.__projects_next_id
            case "tasks":
                return self.__tasks_next_id
            case _:
                raise ValueError("Invalid table")
