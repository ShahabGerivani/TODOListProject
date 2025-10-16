from abc import ABC, abstractmethod
from typing import Any

from src.TODOListProject.models import NamedEntity


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


class InMemoryDB(DBInterface):
    def __init__(self):
        self.projects = {}
        self.tasks = {}

    def get_all(self, table: str) -> list[Any] | None:
        match table:
            case "projects":
                return list(self.projects.values())
            case "tasks":
                return list(self.tasks.values())
            case _:
                raise ValueError("Invalid table")

    def get_by_id(self, table: str, entity_id: int) -> object | None:
        match table:
            case "projects":
                return self.projects[entity_id]
            case "tasks":
                return self.tasks[entity_id]
            case _:
                raise ValueError("Invalid table")

    def update_or_insert(self, table: str, entity: NamedEntity) -> None:
        match table:
            case "projects":
                self.projects[entity.entity_id] = entity
            case "tasks":
                self.tasks[entity.entity_id] = entity
            case _:
                raise ValueError("Invalid table")

    def delete(self, table: str, entity_id: int) -> None:
        match table:
            case "projects":
                del self.projects[entity_id]
            case "tasks":
                del self.tasks[entity_id]
            case _:
                raise ValueError("Invalid table")
