from sqlalchemy import create_engine
from models import Job, Employee, Country, Location, Department, JobHistory
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, NoInspectionAvailable, InvalidRequestError
import os
import sys


class Interface:
    def __init__(self, file_db="", new_db=False, memory_db=False, echo=False):
        if new_db:
            try:
                os.remove(f"{file_db}")
            except FileNotFoundError:
                print("Db file not found.")
        if memory_db:
            self.engine = create_engine("sqlite:///:memory:", echo=echo)
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
                           "Department": ["name", "manager_id", "location_id"],
                           "Location": ["country_name", "city", "street", "postal_code"],
                           "Country": ["name"],
                           "Job": ["title", "min_salary", "max_salary"],
                           "JobHistory": ["employee_id", "start_date", "end_date", "department_id"]}

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

    def update_object(self, table, kwargs):
        session = self.Session()
        try:
            record_id = kwargs["id"]
            update_column = kwargs["update_column"]
            update_value = kwargs["update_value"]
            query = session.query(table).filter_by(id=record_id).update({f"{update_column}": update_value})
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

    # UI elements from here.

    @staticmethod
    def help():
        print("List of commands:\n"
              "- tables - Prints a list of tables.\n"
              "- add - Creates a record in the table.\n"
              "- read - Reads a record from the table.\n"
              "- update - Updates a record from the table.\n"
              "- delete - Deletes a record from the table.\n"
              "- exit - Exits the application..")

    def tables_list(self):
        print("List of tables:")
        for table in self.models:
            print(f"- {table}", end=" ""\n")

    def get_attributes(self, table):
        attributes = ["id"]
        for key in self.attributes[table]:
            attributes.append(key)
        return attributes

    def add(self):
        table = input("Enter table name.\n> ")
        attributes = self.get_attributes(table)
        attributes = attributes[1:]
        table_class = self.models[table]
        print(f"Required attributes: {[a for a in attributes]}")
        kwargs = {}
        for attribute in attributes:
            user_data = input(f"Enter {attribute}: > ")
            kwargs[attribute] = user_data

        self.add_object(table_class, kwargs)
        print(f"Record {kwargs} added to {table} table.")

    def read(self):
        table = input("Enter table name:\n> ")
        attributes = self.get_attributes(table)
        print(f"Available filters: {[a for a in attributes]}")
        data = input("Enter filter type and filter value, eg. 'id 1' or 'name Poland'\n> ")
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
        table = input("Enter table name:\n> ")
        attributes = self.get_attributes(table)
        table = self.models[table]
        record_id = input("Enter record id: > ")
        query = self.read_object(table, {"id": record_id})
        print(f"Record to update: '{query}'")
        print(f"List of attributes: {[a for a in attributes[1:]]}")
        update_column = input("Choose attribute to change: > ")
        update_value = input("Enter new value: > ")
        query_kwargs = {"id": record_id, "update_column": update_column, "update_value": update_value}
        safe = input("Are you sure y/n?\n> ")
        try:
            if safe is "y":
                self.update2(table, query_kwargs)
                print(f"Record {query} {update_column} updated to '{update_value}'")
            else:
                print("Record not updated.")
        except InvalidRequestError:
            print("Invalid attribute.")

    def delete(self):
        table = input("Enter table name:\n> ")
        table = self.models[table]
        record_id = input("Enter record id: > ")
        query = self.read_object(table, {"id": record_id})
        print(f"Record to delete: '{query}'")
        safe = input("Are you sure y/n?\n> ")
        try:
            if safe is "y":
                self.delete_object(table, record_id)
                print(f"Record {query} deleted successfully.")
            else:
                print("Record not deleted.")
        except InvalidRequestError:
            print("Invalid attribute.")

    @staticmethod
    def exit():
        sys.exit(0)

    def ui(self):
        print("Enter 'help' for a list of commands.")
        functions = {"help": self.help, "exit": self.exit, "tables": self.tables_list,
                     "add": self.add, "read": self.read, "update": self.update, "delete": self.delete}
        while True:
            try:
                user_data = input("\nEnter command:\n> ")
                functions[user_data]()
            except NoInspectionAvailable:
                print("No record found.")
            except KeyError:
                print("Invalid command. Use 'help'.")


if __name__ == "__main__":  # UI
    db = Interface(memory_db=True, echo=False)
    db.ui()
