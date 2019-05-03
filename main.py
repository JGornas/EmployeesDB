from sqlalchemy import create_engine
from models import Job, Employee, Country, Location, Department, JobHistory
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, NoInspectionAvailable
import os
import sys


class Interface:
    def __init__(self, file_db="", new_db=False, memory_db=False):
        if new_db:
            try:
                os.remove(f"{file_db}")
            except FileNotFoundError:
                print("Db file not found.")
        if memory_db:
            self.engine = create_engine("sqlite:///:memory:", echo=True)
            print("SQLite::memory: database initiated.")
        else:
            self.engine = create_engine(f"sqlite:///{file_db}", echo=False)
            print(f"SQLite::{file_db}: database initiated.")

        self.tables = [Job, Employee, Country, Location, Department, JobHistory]
        try:
            for table in self.tables:
                table.__table__.create(self.engine)
        except OperationalError:
            print("Tables loaded.")
        self.Session = sessionmaker(bind=self.engine)
        self.models = {"Employee": Employee, "Job": Job, "Location": Location, "Country": Country,
                       "Department": Department, "JobHistory": JobHistory}
        self.attributes = {"Employee": ["first_name", "last_name", "email", "phone_number",
                                        "hire_date", "job_id", "salary", "manager_id", "department_id"],
                           "Department": ["name"], "Location": ["country_name", "city", "street", "postal_code"],
                           "Job": ["title", "min_salary", "max_salary"], "Country": ["name"]}

    def add_object(self, table, kwargs):
        session = self.Session()
        try:
            query = session.add(table(**kwargs))
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return query

    def read_object(self, table, kwargs):
        session = self.Session()
        try:
            query = session.query(table).filter_by(**kwargs).first()
        except:
            session.rollback()
            raise
        finally:
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

    # UI elements below.

    @staticmethod
    def help():
        print(
              "List of commands:\n"
              "- add - Creates a record in table.\n"
              "- read - Reads a record from table.\n"
              "- update - Updates a record from table.\n"
              "- delete - Deletes a record from table.\n"
              "- exit - Exits the app."
             )

    def get_attributes(self, table):
        attributes = ["id"]
        for key in self.attributes[table]:
            attributes.append(key)
        return attributes

    def add(self):
        table = input("Enter table name.\n")
        attributes = self.get_attributes(table)
        attributes = attributes[1:]
        table_class = self.models[table]
        print(f"Attributes required: {[a for a in attributes]}")
        kwargs = {}
        for attribute in attributes:
            user_data = input(f"Enter {attribute}: ")
            kwargs[attribute] = user_data

        self.add_object(table_class, kwargs)
        print(f"Record {kwargs} added to {table} table.")

    def read(self):
        print("List of tables:")
        for table in self.models:
            print(f"{table}", end=" ")
        table = input("\nEnter table name:\n")
        attributes = self.get_attributes(table)
        print(f"Available filters: {[a for a in attributes]}")
        data = input("Enter data: FILTER_TYPE FILTER, eg. 'id 1' or 'name Poland'\n")
        try:
            filter_type, filter_ = data.split(" ")
            table = self.models[table]
            query_kwargs = {filter_type: filter_}
            query = self.read_object(table, query_kwargs)
            print(query)
            return query
        except ValueError:
            print("Invalid data format!")
        print("\n")

    def update(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def exit():
        sys.exit(0)

    def ui(self):
        print("Enter 'help' for a list of commands.")
        functions = {"help": self.help, "exit": self.exit,
                     "add": self.add, "read": self.read, "update": self.update, "delete": self.delete}
        while True:
            try:
                user_data = input("\nEnter command:\n")
                functions[user_data]()
            except NoInspectionAvailable:
                print("No record found.")


if __name__ == "__main__":  # UI
    db = Interface(memory_db=True)
    db.ui()
