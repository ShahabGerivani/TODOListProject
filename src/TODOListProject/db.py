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
        self.__projects = {}
        self.__tasks = {}

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
                self.__projects[entity.entity_id] = entity
            case "tasks":
                self.__tasks[entity.entity_id] = entity
            case _:
                raise ValueError("Invalid table")

    def delete(self, table: str, entity_id: int) -> None:
        match table:
            case "projects":
                del self.__projects[entity_id]
            case "tasks":
                del self.__tasks[entity_id]
            case _:
                raise ValueError("Invalid table")
