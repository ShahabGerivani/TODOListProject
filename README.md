# 📝 TODOListProject

A simple command‑line TODO list manager built with **Python** and **Poetry**.  

## Features

- Create projects with name and description
- Add tasks to projects with name, description, status (todo/doing/done) and deadline
- View, edit and delete tasks and projects
- In-memory database (for now)

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/ShahabGerivani/TODOListProject.git
   cd TODOListProject
   ```

2. **Install dependencies using Poetry**  
   ```bash
   poetry install
   ```

3. **Run the application**  
   ```bash
   poetry run python src/TODOListProject/main.py
   ```
   

## Project Structure

```
TODOListProject/
│
├── src/
│   └── TODOListProject/
│       ├── cli.py            # CLI
│       ├── controller.py     # interface between UI/CLI and data layer
│       ├── db.py             # handles database logic
│       ├── exceptions.py     # custom exceptions
│       ├── main.py           # the app's entry‑point
│       └── models.py         # `Project` and `Task` classes
│
├── .env.example              # Example environment/config variables
├── pyproject.toml            # Poetry configuration and dependencies
├── poetry.lock
└── README.md
```
