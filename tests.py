import unittest
from main import Interface
from models import Job, Employee, Country, Location, Department, JobHistory


class TestApp(unittest.TestCase):

    @classmethod  # runs once at start
    def setUpClass(cls):
        cls.db = Interface("tests.db", new_db=True)

        countries = [{"name": "Poland"},
                     {"name": "France"},
                     {"name": "Germany"}]
        [cls.db.add_object(Country, country) for country in countries]

        locations = [{"street": "Wielka", "postal_code": "50-100", "city": "Lublin", "country_name": "Poland"},
                     {"street": "Angielska", "postal_code": "50-101", "city": "Lublin", "country_name": "Poland"}]
        [cls.db.add_object(Location, location) for location in locations]

        jobs = [{"title": "Manager", "min_salary": "3000", "max_salary": "5000"},
                {"title": "Driver", "min_salary": "1000", "max_salary": "4000"}]
        [cls.db.add_object(Job, job) for job in jobs]

        employees = [{"first_name": "Jan", "last_name": "Nowak", "email": "jnowak@gmail.com",
                      "phone_number": "60 825 23 38", "hire_date": "12.12.12", "job_id": "1",
                      "salary": "2000", "department_id": "1"},
                     {"first_name": "Andrzej", "last_name": "Lisiecki", "email": "lisek@gmail.com",
                      "phone_number": "512 650 222", "hire_date": "13.12.12", "job_id": "2",
                      "manager_id": "1", "salary": "1500", "department_id": "2"}]
        [cls.db.add_object(Employee, employee) for employee in employees]

        departments = [{"name": "Office", "manager_id": "1", "location_id": 1},
                       {"name": "Warehouse", "manager_id": "1", "location_id": 2},
                       {"name": "Shop", "manager_id": "1", "location_id": 2}]
        [cls.db.add_object(Department, department) for department in departments]

    def test_read_by_id(self):
        emp1 = self.db.read_object(Employee, {"id": 1})
        emp2 = self.db.read_object(Employee, {"id": 2})
        country1 = self.db.read_object(Country, {"id": 1})
        country2 = self.db.read_object(Country, {"id": 2})
        self.assertEqual(type(emp1), str)
        self.assertEqual(emp1, "1. Jan. Nowak. jnowak@gmail.com. 60 825 23 38. Hire date: 12.12.12. "
                               "Job id: 1. Salary: 2000. Manager id: None. Department id: 1. ")
        self.assertEqual(emp2, "2. Andrzej. Lisiecki. lisek@gmail.com. 512 650 222. Hire date: 13.12.12. "
                               "Job id: 2. Salary: 1500. Manager id: 1. Department id: 2. ")
        self.assertEqual(country1, "1. Poland.")
        self.assertEqual(country2, "2. France.")

    def test_update_by_id(self):
        query_kwargs = {"id": "2", "update_column": "name", "update_value": "England"}
        self.db.update_object(Country, query_kwargs)
        country = self.db.read_object(Country, {"id": 2})
        self.assertEqual(country, "2. England.")

    def test_delete_by_id(self):
        country = self.db.delete_object(Country, 3)
        self.assertEqual(country, None)
