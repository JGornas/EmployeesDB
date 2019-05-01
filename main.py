from sqlalchemy import create_engine
from models import Job, Employee, Country, Location, Department, JobHistory
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, NoInspectionAvailable
import os
import sys


class Interface:
    def __init__(self, file_db="", new_db=False, memory_db=False):
        if memory_db:
            self.engine = create_engine("sqlite:///:memory:", echo=True)
            print("SQLite::memory: database initiated.")
        else:
            self.engine = create_engine(f"sqlite:///{file_db}", echo=False)
            print(f"SQLite::{file_db}: database initiated.")
        if new_db:
            try:
                os.remove(f"{file_db}")
            except FileNotFoundError:
                print("Db file not found.")
        try:
            for table in [Job, Employee, Country, Location, Department, JobHistory]:
                table.__table__.create(self.engine)
        except OperationalError:
            print("Tables loaded.")
        self.Session = sessionmaker(bind=self.engine)

    def add_object(self, table):
        session = self.Session()
        try:
            query = session.add(table)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return query

    def read_object(self, table, object_id):
        session = self.Session()
        query = session.query(table).filter_by(id=object_id).first()
        session.close()
        return str(query)

    def update_object(self, table, object_id, column, new_value):
        session = self.Session()
        try:
            query = session.query(table).filter_by(id=object_id).update({f"{column}": new_value})
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return query

    def delete_object(self, table, object_id):
        session = self.Session()
        try:
            query = session.query(table).filter_by(id=object_id)
            query2 = query
            query.delete()
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return query2.first()

    def help(self):
        print(
            "List of commands:\n"
            "- add - Creates a record in table.\n"
            "- read - Reads a record from table.\n"
            "- update - Updates a record from table.\n"
            "- delete - Deletes a record from table.\n"
            "- exit - Exits the app.\n"
             )

    def read(self, *args):
        table = input("Enter table name.\n")
        object_id = input("Enter record id\n")
        self.read_object(table=table, object_id=object_id)

    def add(self):
        table = input("Enter table name.\n")
        user_input = input("Enter record data\n")
        models = {"Country": Country}
        func = models[table]
        self.add_object(func(user_input))

    def update(self):
        table = input("Enter table name.\n")
        object_id = input("Enter record id.\n")
        self.read_object(table=table, object_id=object_id)

    def delete(self):
        table = input("Enter table name.\n")
        object_id = input("Enter record id.\n")
        self.read_object(table=table, object_id=object_id)

    def exit(self):
        sys.exit(0)

    def ui(self):
        print("Enter 'help' for commands list.")
        functions = {"help": self.help, "exit": self.exit,
                     "add": self.add, "read": self.read, "update": self.update, "delete": self.delete}
        while True:
            try:
                user_data = input("Enter command:\n")
                functions[user_data]()
            except NoInspectionAvailable:
                print("No record found.")


if __name__ == "__main__":  # dummy data
    db = Interface("employees.db")

    db.add_object(Country(name="Poland"))
    db.add_object(Job(title="Manager", min_salary=1500, max_salary=2000))
    db.add_object(Job(title="Driver", min_salary=1000, max_salary=1700))
    db.add_object(Location(street="Wielka", postal_code="50-100", city="Lublin", country_name="Poland"))
    db.add_object(Location(street="Angielska", postal_code="50-101", city="Lublin", country_name="Poland"))
    db.add_object(Employee(first_name="Jan", last_name="Nowak", email="jnowak@gmail.com",
                           phone_number="60 825 23 38", hire_date="12.12.12",
                           job_id=1, salary=2000, department_id=1))
    db.add_object(Employee(first_name="Andrzej", last_name="Lisiecki", email="lisek@gmail.com",
                           phone_number="512 650 222", hire_date="13.12.12",
                           job_id=2, manager_id= 1, salary=1500, department_id=2))
    db.add_object(Department(name="Office", manager_id=1, location_id=1))
    db.add_object(Department(name="Warehouse", manager_id=1, location_id=2))
    db.ui()