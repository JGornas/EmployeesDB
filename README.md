# Employees_DB

Employees_DB is a command line application for the management of employees database. 

Uses:
Python 3.6,
SQLite database,
SQLAlchemy.

## Installation

Use the package manager pip to install required libraries.

```bash
pip install -r requirements.txt
```

## Usage

Make an instance of UserInterface. It will connect to the choosen database on initialization.
```python
from ui import UserInterface
db = UserInterface(file_db="database.db")
```
UserInterface parameters:
- file_db - Direct path to the database file, eg. "database.db".
- new_db - If true, removes previous db file linked to file_db.
- memory_db - If true, database initiates in memory.
- echo - If true, prints SQL commands in the console.

Start the UI with ui_loop().
```bash
db.ui_loop()

SQLite::memory/file: database initiated.
Enter 'help' for a list of commands.

Enter command:
> ...
```

List of commands:
- tables - Prints a list of tables.
- add - Creates a record in the table.
- read - Reads a record from the table.
- read all - Reads all records from the table.
- update - Updates a record from the table.
- delete - Deletes a record from the table.
- exit - Exits the application.

Adding record:
```bash
Enter command:
> add
Enter table name. > Job
Required attributes: ['title', 'min_salary', 'max_salary']
Enter title: > Accountant
Enter min_salary: > 1200
Enter max_salary: > 4000
Record {'title': 'Accountant', 'min_salary': '1200', 'max_salary': '4000'} added to Job table.
```

Reading record; Use 'read all' for all records in a table.
```bash
Enter command:
> read
Enter table name: > Job
Available filters: ['id', 'title', 'min_salary', 'max_salary']
Enter filter type and filter value, eg. 'id 1' or 'name Poland'
> name Accountant
3. Accountant. Min Salary: 1500. Max Salary: 4000.
```

Updating record:
```bash
Enter command:
> update
Enter table name: > Job
Enter record id: > 3
Record to update: '3. Accountant. Min Salary: 1500. Max Salary: 4000.'
List of attributes: ['title', 'min_salary', 'max_salary']
Choose attribute to change: > min_salary
Enter new value: > 2000
Are you sure y/n? > y
Record 3. Accountant. Min Salary: 1500. Max Salary: 4000. min_salary updated to '2000'.
```

Deleting record:
```bash
Enter command:
> delete
Enter table name: > Job
Enter record id: > 3
Record to delete: '3. Accountant. Min Salary: 2000. Max Salary: 4000.'
Are you sure y/n? > y
Record 3. Accountant. Min Salary: 2000. Max Salary: 4000. deleted successfully.
```

Interface class can further used for GUI.

## License

[MIT](https://choosealicense.com/licenses/mit/)

























