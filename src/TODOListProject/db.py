from abc import ABC, abstractmethod
from typing import Any
from dotenv import load_dotenv
import os
from typing import cast

from src.TODOListProject.exceptions import DBFullError
from src.TODOListProject.models import NamedEntity, Project, Task


class DBInterface(ABC):
    @abstractmethod
    def get_all(self, table: str) -> list | None:
        pass

    @abstractmethod
    def get_by_id(self, table: str, entity_id: int) -> object | None:
        pass

    @abstractmethod
    def update_or_insert(self, table: str, entity: object) -> None:
        pass

    @abstractmethod
    def delete(self, table: str, entity_id: int) -> None:
        pass

    @abstractmethod
    def get_next_id(self, table: str) -> int | None:
        pass


class InMemoryDB(DBInterface):
    def __init__(self):
        self.__projects = {}
        self.__tasks = {}
        self.__projects_next_id = 0
        self.__tasks_next_id = 0
        load_dotenv()
        self.__MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT"))
        self.__MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK"))

    def get_all(self, table: str) -> list[Any] | None:
        match table:
            case "projects":
                return list(self.__projects.values())
            case "tasks":
                return list(self.__tasks.values())
            case _:
                raise ValueError("Invalid table")

    def get_by_id(self, table: str, entity_id: int) -> object | None:
        match table:
            case "projects":
                return self.__projects[entity_id]
            case "tasks":
                return self.__tasks[entity_id]
            case _:
                raise ValueError("Invalid table")

    def update_or_insert(self, table: str, entity: NamedEntity) -> None:
        match table:
            case "projects":
                # Checking for duplicate names
                for existing in self.__projects.values():
                    if existing.name == entity.name and existing.entity_id != entity.entity_id:
                        raise ValueError(f"Project with name '{entity.name}' already exists.")
                # -- Update --
                if entity.entity_id in self.__projects:
                    self.__projects[entity.entity_id] = entity
                    return
                # -- Insert --
                if len(self.__projects) >= self.__MAX_NUMBER_OF_PROJECT:
                    raise DBFullError("Maximum number of projects reached")
                self.__projects[entity.entity_id] = entity
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

    def get_next_id(self, table: str) -> int | None:
        match table:
            case "projects":
                return self.__projects_next_id
            case "tasks":
                return self.__tasks_next_id
            case _:
                raise ValueError("Invalid table")
