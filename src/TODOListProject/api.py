"""FastAPI interface"""
from fastapi import FastAPI, HTTPException

from src.TODOListProject.controller import ProjectTaskController
from src.TODOListProject.db import RelationalDB
from src.TODOListProject.exceptions import DBFullError
from src.TODOListProject.model import models, pydantic_models

app = FastAPI()
controller = ProjectTaskController(RelationalDB("postgresql://postgres:1234@localhost/todolist"))


@app.get("/projects/")
def projects() -> list[pydantic_models.Project]:
    """
    View all projects
    :return: a list of all projects
    """
    projects_list: list[models.Project] = controller.get_all_projects()
    return [pydantic_models.Project(id=p.entity_id, name=p.name, description=p.description, tasks={
        t.entity_id: pydantic_models.Task(id=t.entity_id, project_id=t.project_id, name=t.name,
                                          description=t.description,
                                          status=t.status, deadline=t.deadline)
        for t in p.tasks.values()}) for p in
            projects_list]


@app.get("/projects/{project_id}/tasks/")
def projects_tasks(project_id: int) -> list[pydantic_models.Task]:
    """
    View all tasks for a project
    :param project_id:
    :return: a list of all tasks for a project
    """
    try:
        tasks_list: list[models.Task] = controller.get_all_tasks(project_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Project not found")
    return [pydantic_models.Task(id=t.entity_id, project_id=t.project_id, name=t.name,
                                 description=t.description,
                                 status=t.status, deadline=t.deadline) for t in tasks_list]


@app.post("/projects/")
def add_project(project: pydantic_models.ProjectCreate) -> None:
    """
    Create a new project
    :param project:
    :return:
    """
    try:
        controller.create_project(project.name, project.description)
    except (ValueError, DBFullError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.patch("/projects/{project_id}")
def edit_project(project_id: int, project: pydantic_models.ProjectEdit) -> None:
    """
    Edit an existing project
    :param project_id:
    :param project: An object containing the fields to be changed and their values. If you don't want to change a field, don't include it.
    :return:
    """
    try:
        controller.edit_project(project_id, project.name, project.description)
    except (ValueError, DBFullError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Project not found")


@app.delete("/projects/{project_id}")
def delete_project(project_id: int) -> None:
    """
    Delete an existing project
    :param project_id:
    :return:
    """
    try:
        controller.delete_project(project_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Project not found")


@app.post("/projects/{project_id}/tasks/")
def add_task(project_id: int, task: pydantic_models.TaskCreate) -> None:
    """
    Add a new task for a project
    :param project_id:
    :param task:
    :return:
    """
    try:
        controller.create_task(project_id, task.name, task.description, task.status, task.deadline)
    except (ValueError, DBFullError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Project not found")


@app.patch("/tasks/{task_id}")
def edit_task(task_id: int, task: pydantic_models.TaskEdit) -> None:
    """
    Edit an existing task
    :param task_id:
    :param task: An object containing the fields to be changed and their values. If you don't want to change a field, don't include it.
    :return:
    """
    try:
        controller.edit_task(task_id, task.name, task.description, task.status, task.deadline)
    except (ValueError, DBFullError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> None:
    """
    Delete an existing task
    :param task_id:
    :return:
    """
    try:
        controller.delete_task(task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
