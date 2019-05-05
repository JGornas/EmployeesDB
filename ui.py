from interface import Interface
import sys
from sqlalchemy.exc import NoInspectionAvailable, InvalidRequestError


class UserInterface(Interface):

    @staticmethod
    def help():
        print("List of commands:\n"
              "- tables - Prints a list of tables.\n"
              "- add - Creates a record in the table.\n"
              "- read - Reads a record from the table.\n"
              "- read all - Reads all records from the table.\n"
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

    def read_table(self):
        table = input("Enter table name:\n> ")
        table = self.models[table]
        for search in self.read_all(table):
            print(search)

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
                self.update_object(table, query_kwargs)
                print(f"Record {query} {update_column} updated to '{update_value}'.")
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

    def ui_loop(self):
        print("Enter 'help' for a list of commands.")
        functions = {"help": self.help, "exit": self.exit, "tables": self.tables_list,
                     "add": self.add, "read": self.read, "read all": self.read_table, "update": self.update,
                     "delete": self.delete}
        while True:
            try:
                user_data = input("\nEnter command:\n> ")
                functions[user_data]()
            except NoInspectionAvailable:
                print("No record found.")
            except KeyError:
                print("Invalid command. Use 'help'.")


if __name__ == "__main__":
    ui = UserInterface(memory_db=True, echo=True)
    ui.ui_loop()
