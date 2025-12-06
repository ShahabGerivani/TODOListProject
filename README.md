# 📝 TODOListProject

A simple TODO list manager project made for software design course @ Amirkabir University of Technology 2025-2026.  

## Technologies used

Python, Poetry, FastAPI, PostgreSQL, Alembic, SQLAlchemy ORM

## Features

- Create projects with name and description
- Add tasks to projects with name, description, status (todo/doing/done) and deadline
- View, edit and delete tasks and projects
- Support for in-memory database and also SQL database
- Command line interface and REST API interface
- Auto-close overdue tasks in set intervals

## Try it out

1. **Clone the repository**  
   ```bash
   git clone https://github.com/ShahabGerivani/TODOListProject.git
   cd TODOListProject
   ```

2. **Install dependencies using Poetry**  
   ```bash
   poetry install
   ```

3. **Configure the database**
   ```bash
   docker compose up
   alembic upgrade head
   ```

4. **Run the CLI**  
   ```bash
   poetry run python src/TODOListProject/main.py
   ```

   **Or run the API**
   ```bash
   poetry run fastapi dev api.py
   ```

## Project Structure

```
.
├── alembic.ini
├── docker-compose.yml           # Docker compose file for running a PostgreSQL container
├── poetry.lock
├── pyproject.toml
├── README.md
└── src
    ├── alembic
    └── TODOListProject
        ├── api.py               # REST API Implementation
        ├── autoclose_overdue.py # A script for auto-closing overdue tasks in set intervals
        ├── cli.py               # CLI implementation
        ├── controller.py        # Business logic
        ├── db.py                # Database interface implementations (in-memory & SQL)
        ├── exceptions.py
        ├── main.py              # Main entry point for CLI
        └── model
            ├── models.py
            ├── orm_models.py
            └── pydantic_models.py
```
