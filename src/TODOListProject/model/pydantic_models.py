"""Pydantic data classes to use with fastAPI"""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from src.TODOListProject.model.models import TaskStatus


class Task(BaseModel):
    """Class for returning tasks"""
    id: int
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    description: str
    status: TaskStatus = TaskStatus.todo
    deadline: datetime | None = None
    project_id: int


class TaskCreate(BaseModel):
    """Class representing an input object for creating new tasks"""
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    description: str
    status: TaskStatus = TaskStatus.todo
    deadline: datetime | None = None


class TaskEdit(BaseModel):
    """Class representing an input object for editing tasks"""
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] | None = None
    description: str | None = None
    status: TaskStatus | None = None
    deadline: datetime | None = None


class Project(BaseModel):
    """Class for returning projects"""
    id: int
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    description: str
    tasks: dict[int, Task]


class ProjectCreate(BaseModel):
    """Class representing an input object for creating new projects"""
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    description: str


class ProjectEdit(BaseModel):
    """Class representing an input object for editing projects"""
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)] | None = None
    description: str | None = None
