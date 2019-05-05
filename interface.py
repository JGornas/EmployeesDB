from models import Job, Employee, Country, Location, Department, JobHistory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os


class Interface:
    def __init__(self, file_db="", new_db=False, memory_db=False, echo=False):
        if new_db:  # Forces new database file if true.
            try:
                os.remove(f"{file_db}")
            except FileNotFoundError:
                print("Db file not found.")
        if memory_db:  # Inits database in sqlite:memory.
            self.engine = create_engine("sqlite:///:memory:", echo=echo)
            print("SQLite::memory: database initiated.")
        else:  # Inits database in sqlite:database file.
            self.engine = create_engine(f"sqlite:///{file_db}", echo=False)
            print(f"SQLite::{file_db}: database initiated.")

        self.tables = [Job, Employee, Country, Location, Department, JobHistory]
        try:  # Force new tables.
            for table in self.tables:
                table.__table__.create(self.engine)
        except OperationalError:
            print("Tables loaded.")
        self.Session = sessionmaker(bind=self.engine)

        # Maps user input to db models.
        self.models = {"Employee": Employee, "Job": Job, "Location": Location, "Country": Country,
                       "Department": Department, "JobHistory": JobHistory}
        # All attributes of each table.
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

    def read_all(self, table):
        session = self.Session()
        try:
            query = session.query(table).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return query

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
            query2 = query  # query after .delete returns None.
            query.delete()
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return query2.first()
