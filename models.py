from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(20))
    min_salary = Column(Integer)
    max_salary = Column(Integer)

    def __repr__(self):
        return f"{self.id}. {self.title}. Min. Salary: {self.min_salary}. Max. Salary: {self.min_salary}."


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(15))

    def __repr__(self):
        return f"{self.id}. {self.name}"


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    street = Column(String(20))
    postal_code = Column(String(20))
    city = Column(String(20))
    country_name = Column(Integer, ForeignKey('countries.name'))

    def __repr__(self):
        return f"{self.id}. {self.street}. {self.postal_code}. {self.city}. {self.country_name}."


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    manager_id = Column(Integer, ForeignKey('employees.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))

    def __repr__(self):
        return f"{self.id}. {self.name}. Manager id: {self.manager_id}. Location id: {self.location_id}. "


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(25))
    phone_number = Column(String(20))
    hire_date = Column(String(20))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    salary = Column(Integer)
    manager_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'))

    def __repr__(self):
        return f"{self.id}. {self.first_name}. {self.last_name}. {self.email}. {self.phone_number}. "\
            f"Hire date: {self.hire_date}. Job id: {self.job_id}. Salary: {self.salary}. "\
            f"Manager id: {self.manager_id}. Department id: {self.department_id}. "


class JobHistory(Base):
    __tablename__ = "jobs_history"

    id = Column(Integer, primary_key=True)
    employee_id = Column(String(25))
    start_date = Column(String(25))
    end_date = Column(String(25))
    department_id = Column(Integer, ForeignKey('departments.id'))
