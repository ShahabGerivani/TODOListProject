import src.TODOListProject.cli as cli
from src.TODOListProject.controller import ProjectTaskController
from src.TODOListProject.db import InMemoryDB, RelationalDB

if __name__ == "__main__":
    # cli.run_cli(ProjectTaskController(InMemoryDB()))
    cli.run_cli(ProjectTaskController(RelationalDB('postgresql://postgres:1234@localhost/todolist')))
