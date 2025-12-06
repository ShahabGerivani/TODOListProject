import dateutil.parser

from src.TODOListProject.controller import ProjectTaskController
from src.TODOListProject.model.models import TaskStatus


def handle_view(controller: ProjectTaskController, action: list[str]) -> None:
    """
    Handler function for viewing projects or tasks
    :param controller: Controller instance
    :param action: The input line converted to a list of words (look into run_cli)
    :return:
    """
    if action[1] == "p":
        projects = controller.get_all_projects()
        if len(projects) == 0:
            print("You have no projects")
        else:
            print("Your Projects:")
            for project in controller.get_all_projects():
                print(f"{project.entity_id} {project.name}:\n"
                      f"  description: {project.description}\n")
    elif action[1] == "t":
        try:
            tasks = controller.get_all_tasks(int(action[2]))
            if len(tasks) == 0:
                print("You have no tasks")
            else:
                print(f"Project {action[2]} tasks:")
                for task in tasks:
                    print(f"{task.entity_id} {task.name}:\n"
                          f"  description: {task.description}\n"
                          f"  status: {str(task.status).split(".")[1]}\n"
                          f"  deadline: {task.deadline}\n")
        except IndexError:
            print("Please enter project id")
        except KeyError:
            print("Invalid project id")
    else:
        print("Invalid action")


def handle_add(controller: ProjectTaskController, action: list[str]) -> None:
    """
    Handler function for adding new projects or tasks
    :param controller: Controller instance
    :param action: The input line converted to a list of words (look into run_cli)
    :return:
    """
    if action[1] != "p" and action[1] != "t":
        print("Invalid action")
        return
    if action[1] == "t" and len(action) != 3:
        print("No project id")
        return
    name = ""
    while not name:
        name = input("Please enter name (<= 30 words): ")
    description = input("Please enter description (Optional) (<= 150 words): ")
    if action[1] == "p":
        try:
            controller.create_project(name, description)
            print(f"Project {name} created successfully.")
        except Exception as e:
            print(e)
    elif action[1] == "t":
        deadline = None
        while True:
            try:
                deadline_str = input("Please enter deadline (Optional): ")
                if deadline_str:
                    deadline = dateutil.parser.parse(deadline_str)
                break
            except dateutil.parser.ParserError:
                print("Invalid deadline format")
                continue
        try:
            controller.create_task(int(action[2]), name, description, TaskStatus.todo, deadline)
            print(f"Task {name} added to project {action[2]} successfully.")
        except Exception as e:
            print(e)


def handle_edit(controller: ProjectTaskController, action: list[str]) -> None:
    """
    Handler function for editing projects or tasks
    :param controller: Controller instance
    :param action: The input line converted to a list of words (look into run_cli)
    :return:
    """
    if action[1] != "p" and action[1] != "t":
        print("Invalid action")
        return
    if len(action) != 3:
        print("No id")
        return
    name = input("Please enter new name (<= 30 words) (Leave empty if you don't want to change): ")
    if not name: name = None
    description = input("Please enter new description (<= 150 words) (Leave empty if you don't want to change): ")
    if not description: description = None
    # Project
    if action[1] == "p":
        try:
            controller.edit_project(int(action[2]), name, description)
            print(f"Project {action[2]} updated successfully.")
        except Exception as e:
            print(e)
    # Task
    elif action[1] == "t":
        deadline = None
        while True:
            try:
                deadline_str = input("Please enter new deadline (Leave empty if you don't want to change): ")
                if deadline_str:
                    deadline = dateutil.parser.parse(deadline_str)
                break
            except dateutil.parser.ParserError:
                print("Invalid deadline format")
                continue
        status = None
        status_str = input("Please enter new status (todo/doing/done) (Leave empty if you don't want to change): ")
        while status_str:
            try:
                status = TaskStatus[status_str]
                break
            except KeyError:
                print("Invalid status")
                status_str = input(
                    "Please enter new status (todo/doing/done) (Leave empty if you don't want to change): ")
        try:
            controller.edit_task(int(action[2]), name, description, status, deadline)
            print(f"Task {action[2]} updated successfully.")
        except Exception as e:
            print(e)


def handle_del(controller: ProjectTaskController, action: list[str]) -> None:
    """
    Handler function for deleting projects or tasks
    :param controller: Controller instance
    :param action: The input line converted to a list of words (look into run_cli)
    :return:
    """
    if len(action) != 3:
        print("No id")
        return
    try:
        if action[1] == "p":
            controller.delete_project(int(action[2]))
        elif action[1] == "t":
            controller.delete_task(int(action[2]))
    except KeyError:
        print("Invalid id")


def run_cli(controller: ProjectTaskController):
    """
    The main entry point for the CLI
    :param controller: Controller instance
    :return:
    """
    print("TODO List")
    print("WARNING: CLI interface is deprecated. Please use the FastAPI HTTP interface instead.")
    action: list[str] = ["help"]
    while True:
        # Checking if the input format is correct
        try:
            _ = action[0]
            if action[0] not in ["help", "exit"]:
                _ = action[1]
            valid_input = True
        except IndexError:
            print("Invalid action")
            valid_input = False
        if valid_input:
            match action[0]:
                case "help":
                    print("Options:\n"
                          "help                   View options\n"
                          "view p                 View all projects\n"
                          "view t [project_id]    View all tasks for project with id = [project_id]\n"
                          "add p                  Add new project\n"
                          "edit p [project_id]    Edit project with id = [project_id] \n"
                          "del p [project_id]     Delete project with id = [project_id]\n"
                          "add t [project_id]     Add new task to project with id = [project_id]\n"
                          "edit t [task_id]       Edit task with id = [task_id] \n"
                          "del t [task_id]        Delete task with id = [task_id] \n"
                          "exit                   Exit\n")
                case "view":
                    handle_view(controller, action)
                case "add":
                    handle_add(controller, action)
                case "edit":
                    handle_edit(controller, action)
                case "del":
                    handle_del(controller, action)
                case "exit":
                    exit(0)
                case _:
                    print("Invalid action")
        action = input("What do you want to do? (enter help to view options) ").lower().split()
