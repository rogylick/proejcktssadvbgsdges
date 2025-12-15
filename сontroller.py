from .model import Model
from .view import View
from functools import wraps
from psycopg2.errors import StringDataRightTruncation


def catch_db_error(option):
    @wraps(option)
    def inner(self, *args, **kwargs):
        try:
            option(self, *args, **kwargs)
        except (IndexError, StringDataRightTruncation, ValueError, AssertionError) as e:
            print(f"\n Known DB error: {type(e).__name__} — {e}\n")
            self.view.output_error_message()
        except Exception as e:
            print(f"\n Unexpected error in {option.__name__}: {type(e).__name__} — {e}\n")
            self.view.output_error_message()
    return inner


class Controller:
    def __init__(self):
        self.available = {
            "create": {
                "product": self.create_product,
                "material": self.create_material,
                "consumation": self.create_consumation,
            },
            "read": {
                "product": self.read,
                "material": self.read,
                "consumation": self.read,
            },
            "update": {
                "product": self.update_product,
                "material": self.update_material,
                "consumation": self.update_consumation,
            },
            "delete": {
                "product": self.delete_product,
                "material": self.delete_material,
                "consumation": self.delete_consumation,
            },
            "task_2": {
                "generate_products": self.task_generate_products,
                "generate_materials": self.task_generate_materials,
                "generate_consumations": self.task_generate_consumations,

            },
            "task_3": {
                "search_products": self.task3_search_products,
                "search_materials": self.task3_search_materials,
                "search_consumations": self.task3_search_consumptions,
            },
        }
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            chosen_mode_viewer, chosen_mode = self.view.show_menu()
            if not chosen_mode_viewer:
                self.model.disconnect()
                break
            chosen_option_viewer, chosen_option = chosen_mode_viewer()
            args_or_command = chosen_option_viewer()

            # call mapped function
            self.available[chosen_mode][chosen_option](args_or_command)

    # --- CREATE ---
    @catch_db_error
    def create_product(self, args):
        name, description = args
        self.model.create_product(name, description)

    @catch_db_error
    def create_material(self, args):
        name, unit, price = args
        self.model.create_material(name, unit, price)

    @catch_db_error
    def create_consumation(self, args):
        product1_id, material_id, quantity = args
        self.model.create_consumation(product1_id, material_id, quantity)

    # --- READ ---
    def read(self, read_from):
        original_name = read_from
        
        
        # Створюємо мапу відповідності: [те, що приходить з View] -> [ключ у Model]
        table_mapping = {
            "product": "product",
            "material": "material",
            "consumation": "consumation"
        }


        db_table_name = table_mapping.get(read_from)
        
        if not db_table_name:
            print(f"[ERROR] Unknown table key: {read_from}")
            self.view.output_error_message()
            return
            
        try:
            table = self.model.read(db_table_name)
            self.view.output_table(table, original_name)
        except Exception as e:
            print(f"[ERROR] Database error during READ: {e}")
            self.view.output_error_message()

    # --- UPDATE ---
    @catch_db_error
    def update_product(self, args):
        prod_id, what_to_change, new_value = args
        field_map = {
            "name": "name",
            "description": "description",
        }
        field = field_map.get(what_to_change)
        if not field:
            raise ValueError(f"Unknown field: {what_to_change}")
        affected = self.model.update_field("product", int(prod_id), field, new_value)
        if affected == 0:
            print(f"[INFO] No Product with id={prod_id} — nothing was updated.")
        else:
            print(f"[SUCCESS] Product id={prod_id} updated: set {field} = {new_value}")

    @catch_db_error
    def update_material(self, args):
        mat_id, what_to_change, new_value = args
        field_map = {
            "name": "name",
            "unit": "unit",
            "price_per_unit": "price_per_unit",
        }
        field = field_map.get(what_to_change)
        if not field:
            raise ValueError(f"Unknown field: {what_to_change}")
        # convert price to numeric if needed
        if field == "price_per_unit":
            new_value = float(new_value)
        affected = self.model.update_field("material", int(mat_id), field, new_value)
        if affected == 0:
            print(f"[INFO] No material with id={mat_id} — nothing was updated.")
        else:
            print(f"[SUCCESS] Material id={mat_id} updated: set {field} = {new_value}")

    @catch_db_error
    def update_consumation(self, args):
        cons_id, what_to_change, new_value = args
        field_map = {
            "product1_id": "product1_id",
            "material_id": "material_id",
            "quatity": "quatity",
        }
        field = field_map.get(what_to_change)
        if not field:
            raise ValueError(f"Unknown field: {what_to_change}")
        if field in ("product1_id", "material_id"):
            new_value = int(new_value)
        if field == "quatity":
            new_value = float(new_value)
        affected = self.model.update_field("consumation", int(cons_id), field, new_value)
        if affected == 0:
            print(f"[INFO] No consumption with id={cons_id} — nothing was updated.")
        else:
            print(f"[SUCCESS] Consumption id={cons_id} updated: set {field} = {new_value}")

    # --- DELETE ---
    @catch_db_error
    def delete_product(self, record_id):
         self.model.delete("product", int(record_id))

    @catch_db_error
    def delete_material(self, record_id):
        self.model.delete("material", int(record_id))

    @catch_db_error
    def delete_consumation(self, record_id):
        self.model.delete("consumation", int(record_id))

    # --- TASK 2: GENERATION ---
    @catch_db_error
    def task_generate_products(self, args):
        n = int(args)
        print(f"[TASK2] Generating {n} products...")
        created = self.model.generate_products(n)
        print(f"[TASK2] Products inserted (approx): {created}")

    @catch_db_error
    def task_generate_materials(self, args):
        n = int(args)
        print(f"[TASK2] Generating {n} materials...")
        created = self.model.generate_materials(n)
        print(f"[TASK2] Materials inserted (approx): {created}")

    @catch_db_error
    def task_generate_consumations(self, args):
        n = int(args)
        print(f"[TASK2] Generating {n} consumption records...")
        created = self.model.generate_consumations(n)
        print(f"[TASK2] Consumptions inserted (approx): {created}")

    # --- TASK 3: SEARCH ---
    @catch_db_error
    def task3_search_products(self, args):

        table, ms = self.model.search_products(*args)
        self.view.output_table(table, "products")
        print(f"[TIME] Query executed in {ms:.3f} ms")

    @catch_db_error
    def task3_search_materials(self, args):
        # args: name_like, price_min_max
        table, ms = self.model.search_materials(*args)
        self.view.output_table(table, "materials")
        print(f"[TIME] Query executed in {ms:.3f} ms")

    @catch_db_error
    def task3_search_consumptions(self, args):
        # args: product_like, material_like, qty_min_max
        table, ms = self.model.search_consumation(*args)
        self.view.output_table(table, "consumptions")
        print(f"[TIME] Query executed in {ms:.3f} ms")
