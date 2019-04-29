from sqlalchemy import create_engine
from models import Job, Employee, Country, Location, Department, JobHistory
from sqlalchemy.orm import sessionmaker
import os


class Interface:
    def __init__(self, file_db="", fresh_db=True, memory_db=False):
        if fresh_db:  # Forces new db file. Creates all tables.
            os.remove("employees.db")
            for table in [Job, Employee, Country, Location, Department, JobHistory]:
                table.__table__.create(engine)
        if memory_db:
            self.engine = create_engine("sqlite:///:memory:", echo=True)
        else:
            self.engine = create_engine(f"sqlite:///{file_db}", echo=True)
        self.Session = sessionmaker(bind=engine)

    def add_object(self, table):
        session = self.Session()
        session.add(table)
        session.commit()


def create_table(model):
    model.__table__.create(engine)


def init_db():
    for table in TABLES:
        create_table(table)

    """Dummy data."""
    add_object(Country(name="Poland"))
    add_object(Job(title="Manager", min_salary=1500, max_salary=2000))
    add_object(Job(title="Driver", min_salary=1000, max_salary=1700))
    add_object(Location(street="Wielka", postal_code="50-100", city="Lublin", country_name="Poland"))
    add_object(Location(street="Angielska", postal_code="50-101", city="Lublin", country_name="Poland"))
    add_object(Employee(first_name="Jan", last_name="Nowak", email="jnowak@gmail.com", phone_number="60 825 23 38",
                        hire_date="12.12.12", job_id=1, salary=2000, department_id=1))
    add_object(Employee(first_name="Andrzej", last_name="Lisiecki", email="lisek@gmail.com", phone_number="512 650 222",
                        hire_date="13.12.12", job_id=2, manager_id= 1, salary=1500, department_id=2))
    add_object(Department(name="Office", manager_id=1, location_id=1))
    add_object(Department(name="Warehouse", manager_id=1, location_id=2))
    read_object(Employee)
    read_object(Job)


def add_object(table):
    session = Session()
    session.add(table)
    session.commit()


def update_object():
    pass


def read_object(table):
    session = Session()
    result = session.query(table).all()
    for r in result:
        print(r)


def delete_object():
    pass


# init_db()
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
