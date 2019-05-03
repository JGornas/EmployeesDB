from models import Job, Employee, Country, Location, Department
from interface import Interface


def main(new_database=False):
    """Connects to database and insert dummy data."""
    if new_database:
        db = Interface("employees.db", new_db=True)
        countries = [{"name": "Poland"},
                     {"name": "France"},
                     {"name": "Germany"}]
        [db.add_object(Country, country) for country in countries]

        locations = [{"street": "Wielka", "postal_code": "50-100", "city": "Lublin", "country_name": "Poland"},
                     {"street": "Angielska", "postal_code": "50-101", "city": "Lublin", "country_name": "Poland"}]
        [db.add_object(Location, location) for location in locations]

        jobs = [{"title": "Manager", "min_salary": "3000", "max_salary": "5000"},
                {"title": "Driver", "min_salary": "1000", "max_salary": "4000"}]
        [db.add_object(Job, job) for job in jobs]

        employees = [{"first_name": "Jan", "last_name": "Nowak", "email": "jnowak@gmail.com",
                      "phone_number": "60 825 23 38", "hire_date": "12.12.12", "job_id": "1",
                      "salary": "2000", "department_id": "1"},
                     {"first_name": "Andrzej", "last_name": "Lisiecki", "email": "lisek@gmail.com",
                      "phone_number": "512 650 222", "hire_date": "13.12.12", "job_id": "2",
                      "manager_id": "1", "salary": "1500", "department_id": "2"}]
        [db.add_object(Employee, employee) for employee in employees]

        departments = [{"name": "Office", "manager_id": "1", "location_id": 1},
                       {"name": "Warehouse", "manager_id": "1", "location_id": 2},
                       {"name": "Shop", "manager_id": "1", "location_id": 2}]
        [db.add_object(Department, department) for department in departments]

        db.ui()  # starts UI loop.
    else:
        db = Interface("employees.db")
        db.ui()


if __name__ == "__main__":
    """New_database is bool for fresh db file."""
    main(new_database=False)
