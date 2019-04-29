from sqlalchemy import create_engine
from models import Job, Employee, Country, Location, Department, JobHistory
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os


class Interface:
    def __init__(self, file_db="", new_db=True, memory_db=False):
        if memory_db:
            self.engine = create_engine("sqlite:///:memory:", echo=True)
        else:
            self.engine = create_engine(f"sqlite:///{file_db}", echo=False)
        if new_db:
            try:
                os.remove(f"{file_db}")
            except FileNotFoundError:
                print("Db file not found.")
        try:
            for table in [Job, Employee, Country, Location, Department, JobHistory]:
                table.__table__.create(self.engine)
        except OperationalError:
            print("Tables initiated.")
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
        query = session.query(table).filter_by(id=object_id).all()
        session.close()
        return query

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
            query.delete()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return query


if __name__ == "__main__":
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

    emp1 = db.read_object(Employee, 1)
    print(emp1)

    db.delete_object(Employee, 2)

    db.update_object(Employee, 1, "first_name", "Kuba")

    emp1 = db.read_object(Employee, 1)
    print(emp1)

    emp2 = db.read_object(Employee, 2)
    print(emp2)
