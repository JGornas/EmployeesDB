# Employees_DB

Employees_DB is a command line database app that works with SQLite database using Python 3.6+ and SQLAlchemy.

## Installation

Use the package manager pip to install required libraries.

```bash
pip install -r requirements.txt
```

## Usage

Main class Interface in interface.py. It can be used with python shell or in-build command line.
Initiate db with:
```python
from ui import UserInterface
db = UserInterface("database.db")
db.ui_loop()
```
List of commands:
- tables - Prints a list of tables.
- add - Creates a record in the table.
- read - Reads a record from the table.
- read all - Reads all records from the table.
- update - Updates a record from the table.
- delete - Deletes a record from the table.
- exit - Exits the application.

```bash
Enter command:
> add
Enter table name.
> Job
Required attributes: ['title', 'min_salary', 'max_salary']
Enter title: > manager
Enter min_salary: > 1000
Enter max_salary: > 1500
Record {'title': 'manager', 'min_salary': '1000', 'max_salary': '1500'} added to Job table.
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
