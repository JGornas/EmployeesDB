from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(20))
    min_salary = Column(Integer)
    max_salary = Column(Integer)

    def __repr__(self):
        return f"{self.id} : {self.title}"


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(15))


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    street = Column(String(20))
    postal_code = Column(String(20))
    city = Column(String(20))
    country_id = Column(Integer, ForeignKey('countries.id'))


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(25))
    phone_number = Column(String(20))
    hire_date = Column(String(20))
    job_id = Column(Integer, ForeignKey('employees.id'))
    salary = Column(Integer)


class JobHistory:
    __tablename__ = "jobs_history"

    id = Column(Integer, primary_key=True)





