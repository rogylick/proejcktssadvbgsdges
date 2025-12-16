from typing import Callable, Union
from tabulate import tabulate


class View:

    def __init__(self):
        self.available_commands_menus: dict = {
            
            "create": self.show_menu_create,
            "read": self.show_menu_read,
            "update": self.show_menu_update,
            "delete": self.show_menu_delete,
            "task_2": self.show_task2_menu,
            "task_3": self.show_task3_menu,
            "quit": None,
        }

        # --- CREATE ---
        self.available_create: dict = {
            "product": self.show_create_product,
            "material": self.show_create_material,
            "consumation": self.show_create_consumation,
        }

        # --- READ ---
        self.available_read: dict = {
            "product": self.show_read_products,
            "material": self.show_read_materials,
            "consumation": self.show_read_consumations,
        }

        # --- UPDATE ---
        self.available_update: dict = {
            "product": self.show_update_product,
            "material": self.show_update_material,
            "consumation": self.show_update_consumation,
        }

        # --- DELETE ---
        self.available_delete: dict = {
            "product": self.show_delete_product,
            "material": self.show_delete_material,
            "consumation": self.show_delete_consumation,
        }

        # --- TASK 2 ---
        self.available_task2: dict = {
            "generate_products": self.show_task2_generate_products,
            "generate_materials": self.show_task2_generate_materials,
            "generate_consumations": self.show_task2_generate_consumations,
        }

        # --- TASK 3 ---
        self.available_task3: dict = {
            "search_consumations": self.show_task3_search_consumations,
        }

        # --- TABLE HEADERS ---
        self.table_headers: dict = {
          "product": ("id", "name", "description"),
          "material": ("id", "name", "price_per_unit", "unit"),
          "consumation": ("id", "product1_id", "material_id", "quatity"),
        }


    # ----------- TABLE OUTPUT -----------

    def output_table(self, table, table_name):
        print("\n\n")
        print(
            tabulate(
                [[field.strip() if isinstance(field, str) else field for field in row] for row in table],
                headers=self.table_headers[table_name]
            )
        )

    @staticmethod
    def output_error_message():
        print("!Incorrect input!")

    # ---------- Menu Helpers ----------

    @staticmethod
    def _output_options(options_dict: dict, amount_of_tabs: int, title: str) -> None:
        options = tuple(options_dict.keys())
        tab_string = "\t" * amount_of_tabs
        print(f"\n\n{tab_string}{title}:\n")
        for index, option in enumerate(options):
            print(f"{tab_string}{index + 1}. {option}\n")

    @staticmethod
    def _handle_wrong_input(options: dict) -> Union[Callable, str]:
        while True:
            try:
                keys = tuple(options.keys())
                option = keys[int(input("Input option number: ").strip()) - 1]
                return options[option]
            except (IndexError, ValueError):
                print("There is no such option, try again")

    @staticmethod
    def _get_key_by_value(dct: dict, value):
        keys = tuple(dct.keys())
        vals = tuple(dct.values())
        return keys[vals.index(value)]

    # ----------- MAIN MENU -----------

    def show_menu(self) -> tuple[Callable, str]:
        self._output_options(self.available_commands_menus, 0, "Select action")
        response = self._handle_wrong_input(self.available_commands_menus)
        return response, self._get_key_by_value(self.available_commands_menus, response)

    # ----------- CREATE -----------

    def show_menu_create(self):
        self._output_options(self.available_create, 1, "Choose what to create")
        response = self._handle_wrong_input(self.available_create)
        return response, self._get_key_by_value(self.available_create, response)

    @staticmethod
    def show_create_product():
        name = input("Enter product name: ")
        description = input("Enter description: ")
        return name, description

    @staticmethod
    def show_create_material():
        name = input("Enter material name: ")
        price_per_unit = input("Enter price per unit: ")
        unit = input("Enter unit:")
        return name, price_per_unit, unit

    @staticmethod
    def show_create_consumation():
        product1_id = input("Enter product ID: ")
        material_id = input("Enter material ID: ")
        quantity = input("Enter quanity used: ")
        return product1_id, material_id, quantity

    # ----------- READ -----------

    def show_menu_read(self):
        self._output_options(self.available_read, 1, "Choose what to read")
        response = self._handle_wrong_input(self.available_read)
        return response, self._get_key_by_value(self.available_read, response)

    @staticmethod
    def show_read_products():
        return "product"

    @staticmethod
    def show_read_materials():
        return "material"

    @staticmethod
    def show_read_consumations():
        return "consumation"

    # ----------- UPDATE -----------

    def show_menu_update(self):
        self._output_options(self.available_update, 1, "Choose what to update")
        response = self._handle_wrong_input(self.available_update)
        return response, self._get_key_by_value(self.available_update, response)

    def show_update_product(self):
        pid = input("Enter product ID: ")
        change_options = {
            "change_name": "name",
            "change_description": "description",
        }
        self._output_options(change_options, 2, "Choose field to update")
        field = self._handle_wrong_input(change_options)
        new_val = input("Enter new value: ")
        return pid, field, new_val

    def show_update_material(self):
        mid = input("Enter material ID: ")
        change_options = {
            "change_name": "name",
            "change_priсe_per_unit": "priсe_per_unit",
            "change_unit": "unit",
        }
        self._output_options(change_options, 2, "Choose field to update")
        field = self._handle_wrong_input(change_options)
        new_val = input("Enter new value: ")
        return mid, field, new_val

    def show_update_consumation(self):
        cid = input("Enter consumation ID: ")
        change_options = {
            "change_product": "product_id",
            "change_material": "material_id",
            "change_quantity": "quatity",
        }
        self._output_options(change_options, 2, "Choose field to update")
        field = self._handle_wrong_input(change_options)
        new_val = input("Enter new value: ")
        return cid, field, new_val

    # ----------- DELETE -----------

    def show_menu_delete(self):
        self._output_options(self.available_delete, 1, "Choose what to delete")
        response = self._handle_wrong_input(self.available_delete)
        return response, self._get_key_by_value(self.available_delete, response)

    @staticmethod
    def show_delete_product():
        return input("Enter product ID: ")

    @staticmethod
    def show_delete_material():
        return input("Enter material ID: ")

    @staticmethod
    def show_delete_consumation():
        return input("Enter consumation ID: ")

    # ----------- TASK 2 (GENERATE) -----------

    def show_task2_menu(self):
        self._output_options(self.available_task2, 1, "Choose what to generate")
        response = self._handle_wrong_input(self.available_task2)
        return response, self._get_key_by_value(self.available_task2, response)

    @staticmethod
    def _gen():
        while True:
            try:
                n = int(input("Enter number to generate: "))
                assert n > 0
                return n
            except (AssertionError, ValueError):
                print("Enter positive integer!")

    def show_task2_generate_products(self):
        return self._gen()

    def show_task2_generate_materials(self):
        return self._gen()

    def show_task2_generate_consumations(self):
        return self._gen()

    # ----------- TASK 3 (SEARCH) -----------

    def show_task3_menu(self):
        self._output_options(self.available_task3, 1, "Choose search query")
        response = self._handle_wrong_input(self.available_task3)
        return response, self._get_key_by_value(self.available_task3, response)

    @staticmethod
    def show_task3_search_consumations():
        pid = input("Enter product ID or '-' for all: ")
        mid = input("Enter material ID or '-' for all: ")
        return pid, mid
