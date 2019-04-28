import sqlalchemy
from models import Job, Employee, Country, Location, Department
from sqlalchemy.orm import sessionmaker

# engine = sqlalchemy.create_engine("sqlite:///employees.db", echo=True)
engine = sqlalchemy.create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker(bind=engine)


def create_table(model):
    model.__table__.create(engine)


def init_db():
    create_table(Job)
    create_table(Country)
    add_object(Country(name="Poland"))
    add_object(Job(title="Manager", min_salary=2000, max_salary=2000))


def add_object(table):
    session = Session()
    session.add(table)
    session.commit()


def update_object():
    pass


def read_object():
    pass


def delete_object():

def add_job(job_name, min_salary, max_salary):
    session = Session()
    job = Job(title=job_name, min_salary=min_salary , max_salary=max_salary)
    session.add(job)
    session.commit()


def add_country(name):
    session = Session()
    country = Country(name=name)
    session.add(country)
    session.commit()


def add_location(street, postal_code, city, country_name):
    session = Session()
    location = Location(street=street, postal_code=postal_code, city=city, country_name=country_name)
    session.add(location)
    session.commit()



def add_employee(firstName, lastName, email, job_id, manager_id):
    pass


init_db()
