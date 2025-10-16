from datetime import datetime
from enum import Enum


class NamedEntity:
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
        if len(value.split()) >= 30:
            raise ValueError("Name too long")
        self.__name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        if len(value.split()) >= 150:
            raise ValueError("Description too long")
        self.__description = value


class Project(NamedEntity):
    def __init__(self, project_id: int, name: str, description: str):
        super().__init__(project_id, name, description)
        self.tasks = []


class TaskStatus(Enum):
    todo = 1
    doing = 2
    done = 3


class Task(NamedEntity):
    def __init__(self, task_id: int, name: str, description: str, project: Project,
                 status: TaskStatus = TaskStatus.todo,
                 deadline: datetime = None):
        super().__init__(task_id, name, description)
        self.__project = project
        self.status = status
        self.deadline = deadline
        project.tasks.append(self)

    @property
    def project(self):
        return self.__project

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
    def deadline(self, value: datetime):
        self.__deadline = value
