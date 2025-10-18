"""Data Models"""

from datetime import datetime
from enum import Enum


class NamedEntity:
    """Base class for Project and Task"""
    def __init__(self, entity_id: int, name: str, description: str):
        self.entity_id = entity_id
        self.name = name
        self.description = description

    @property
    def entity_id(self):
        return self.__entity_id

    @entity_id.setter
    def entity_id(self, value):
        self.__entity_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        """
        :raises ValueError: If name is more than 30 words
        :param value:
        :return:
        """
        if len(value.split()) >= 30:
            raise ValueError("Name too long")
        self.__name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        """
        :raises ValueError: If description is more than 150 words
        :param value:
        :return:
        """
        if len(value.split()) >= 150:
            raise ValueError("Description too long")
        self.__description = value


class Project(NamedEntity):
    def __init__(self, project_id: int, name: str, description: str):
        super().__init__(project_id, name, description)
        self.tasks: dict[int, Task] = {}


class TaskStatus(Enum):
    todo = 1
    doing = 2
    done = 3


class Task(NamedEntity):
    def __init__(self, task_id: int, project_id: int, name: str, description: str, status: TaskStatus,
                 deadline: datetime):
        super().__init__(task_id, name, description)
        self.__project_id = project_id
        self.status = status
        self.deadline = deadline

    @property
    def project_id(self):
        return self.__project_id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: TaskStatus):
        self.__status = value

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, value: datetime | None):
        """
        :raises ValueError: If deadline is in the past
        :param value:
        :return:
        """
        if value is not None and value < datetime.now():
            raise ValueError("Deadline must be in the future")
        self.__deadline = value
