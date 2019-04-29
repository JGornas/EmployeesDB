from sqlalchemy import create_engine, update
from models import Job, Employee, Country, Location, Department, JobHistory
from sqlalchemy.orm import sessionmaker
import os


class Interface:
    def __init__(self, file_db="", fresh_db=True, memory_db=False):
        if memory_db:
            self.engine = create_engine("sqlite:///:memory:", echo=True)
        else:
            self.engine = create_engine(f"sqlite:///{file_db}", echo=True)
        if fresh_db:  # Forces new db file. Creates all tables.
            os.remove("employees.db")
            for table in [Job, Employee, Country, Location, Department, JobHistory]:
                table.__table__.create(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_object(self, table):
        session = self.Session()
        session.add(table)
        session.commit()

    def read_object(self, table, object_id):
        session = self.Session()
        return session.query(table).filter_by(id=object_id).all()

    def update_object(self, table, object_id, column, new_value):
        session = self.Session()
        session.query(table).filter_by(id=object_id).update({f"{column}": new_value})
        session.commit()

    def delete_object(self, table, object_id):
        session = self.Session()
        query = session.query(table).filter_by(id=object_id)
        query.delete()
        session.commit()


db_interface = Interface("employees.db")

db_interface.add_object(Country(name="Poland"))
db_interface.add_object(Job(title="Manager", min_salary=1500, max_salary=2000))
db_interface.add_object(Job(title="Driver", min_salary=1000, max_salary=1700))
db_interface.add_object(Location(street="Wielka", postal_code="50-100", city="Lublin", country_name="Poland"))
db_interface.add_object(Location(street="Angielska", postal_code="50-101", city="Lublin", country_name="Poland"))
db_interface.add_object(Employee(first_name="Jan", last_name="Nowak", email="jnowak@gmail.com",
                                 phone_number="60 825 23 38", hire_date="12.12.12",
                                 job_id=1, salary=2000, department_id=1))
db_interface.add_object(Employee(first_name="Andrzej", last_name="Lisiecki", email="lisek@gmail.com",
                                 phone_number="512 650 222", hire_date="13.12.12",
                                 job_id=2, manager_id= 1, salary=1500, department_id=2))
db_interface.add_object(Department(name="Office", manager_id=1, location_id=1))
db_interface.add_object(Department(name="Warehouse", manager_id=1, location_id=2))

emp1 = db_interface.read_object(Employee, 1)
print(emp1)
db_interface.delete_object(Employee, 2)
db_interface.update_object(Employee, 1, "first_name", "Kuba")
emp1 = db_interface.read_object(Employee, 1)
print(emp1)

emp2 = db_interface.read_object(Employee, 2)
print(emp2)
