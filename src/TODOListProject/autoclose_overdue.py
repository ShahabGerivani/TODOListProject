"""Script to auto close overdue tasks"""
import os
from datetime import datetime

import schedule
from dotenv import load_dotenv

from src.TODOListProject.controller import ProjectTaskController
from src.TODOListProject.db import RelationalDB
from src.TODOListProject.model.models import Project, TaskStatus


def close_overdue(controller: ProjectTaskController) -> None:
    projects: list[Project] = controller.get_all_projects()
    for project in projects:
        for task in project.tasks.values():
            if task.status != TaskStatus.done and task.deadline < datetime.now():
                controller.edit_task(task.entity_id, status=TaskStatus.done)
                print(f"Task {task.entity_id} closed at {datetime.now()}")


if __name__ == "__main__":
    ptc = ProjectTaskController(RelationalDB("postgresql://postgres:1234@localhost/todolist"))
    load_dotenv()
    print(os.getenv("AUTOCLOSE_OVERDUE_RATE_SEC"))
    schedule.every(int(os.getenv("AUTOCLOSE_OVERDUE_RATE_SEC"))).seconds.do(close_overdue, ptc)
    while True:
        schedule.run_pending()
