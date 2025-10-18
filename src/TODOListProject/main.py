import src.TODOListProject.cli as cli
from src.TODOListProject.controller import ProjectTaskController
from src.TODOListProject.db import InMemoryDB

if __name__ == "__main__":
    cli.run_cli(ProjectTaskController(InMemoryDB()))
