from psycopg2 import connect
import time


class Model:
    def __init__(self):
        self.connection = connect(
            database="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432",
        )

        # ---------- INSERT ----------
        self.insert_queries = {
            "product": 'INSERT INTO "Product"(name, description) VALUES (%s, %s)',
            "material": 'INSERT INTO material(name, price_per_unit, unit) VALUES (%s, %s, %s)',
            "consumation": 'INSERT INTO "Consumation"(product1_id, material_id, quatity) VALUES (%s, %s, %s)',
        }

        # ---------- READ ----------
        self.read_queries = {
            "product": 'SELECT id, name, description FROM "Product"',
            "material": 'SELECT id, name, price_per_unit, unit FROM material',
            "consumation": """
                SELECT
                    c.id,
                    p.name AS product,
                    m.name AS material,
                    c.quatity
                FROM "Consumation" c
                JOIN "Product" p ON c.product1_id = p.id
                JOIN material m ON c.material_id = m.id
                ORDER BY c.id
            """
        }

        # ---------- DELETE ----------
        self.delete_queries = {
            "product": 'DELETE FROM "Product" WHERE id = %s',
            "material": 'DELETE FROM material WHERE id = %s',
            "consumation": 'DELETE FROM "Consumation" WHERE id = %s',
        }

        # ---------- UPDATE ----------
        self.update_queries = {
            "product": {
                "name": 'UPDATE "Product" SET name = %s WHERE id = %s',
                "description": 'UPDATE "Product" SET description = %s WHERE id = %s',
            },
            "material": {
                "name": 'UPDATE material SET name = %s WHERE id = %s',
                "price_per_unit": 'UPDATE material SET price_per_unit = %s WHERE id = %s',
                "unit": 'UPDATE material SET unit = %s WHERE id = %s',
            },
            "consumation": {
                "product1_id": 'UPDATE "Consumation" SET product1_id = %s WHERE id = %s',
                "material_id": 'UPDATE "Consumation" SET material_id = %s WHERE id = %s',
                "quatity": 'UPDATE "Consumation" SET quatity = %s WHERE id = %s',
            },
        }

    # ==================== BASIC ====================

    def disconnect(self):
        if self.connection and self.connection.closed == 0:
            self.connection.close()

    def _execute_select(self, query, data=None):
        cur = self.connection.cursor()
        try:
            cur.execute(query, data or ())
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print("\nSELECT ERROR:", e)
            self.connection.rollback()
            return []
        finally:
            cur.close()

    def _execute_modify(self, query, data):
        cur = self.connection.cursor()
        try:
            cur.execute(query, data)
            self.connection.commit()
            return cur.rowcount
        except Exception as e:
            print("\nMODIFY ERROR:", e)
            self.connection.rollback()
            return 0
        finally:
            cur.close()

    # ==================== CREATE ====================

    def create_product(self, name, description):
        return self._execute_modify(self.insert_queries["product"], (name, description))

    def create_material(self, name, ppu, unit):
        return self._execute_modify(self.insert_queries["material"], (name, ppu, unit))

    def create_consumation(self, product_id, material_id, qty):
        return self._execute_modify(
            self.insert_queries["consumation"],
            (product_id, material_id, qty)
        )

    # ==================== READ ====================

    def read(self, table):
        return self._execute_select(self.read_queries[table])

    # ==================== UPDATE ====================

    def update_field(self, table, record_id, field, value):
        query = self.update_queries[table].get(field)
        if not query:
            raise ValueError(f"Unknown field {field} for table {table}")
        return self._execute_modify(query, (value, record_id))

    # ==================== DELETE ====================

    def delete(self, table, record_id):
        return self._execute_modify(self.delete_queries[table], (record_id,))

    # ==================== SEARCH ====================

    def search_consumation(self, product_like, material_like):
        sql = """
        SELECT
            c.id,
            p.name AS product,
            m.name AS material,
            c.quatity
        FROM "Consumation" c
        JOIN "Product" p ON c.product1_id = p.id
        JOIN material m ON c.material_id = m.id
        WHERE
            (%s = '' OR p.name ILIKE %s)
        AND
            (%s = '' OR m.name ILIKE %s)
        ORDER BY c.id
        """

        args = [
            product_like, f"%{product_like}%",
            material_like, f"%{material_like}%"
        ]

        t0 = time.time()
        rows = self._execute_select(sql, args)
        ms = (time.time() - t0) * 1000

        return rows, ms

    # ==================== GENERATORS ====================

    def generate_products(self, n):
        sql = """
        INSERT INTO "Product"(name, description)
        SELECT
         chr((65 + floor(random()*26))::int) ||
         chr((65 + floor(random()*26))::int) ||
         chr((65 + floor(random()*26))::int),
        'Auto-generated description'
        FROM generate_series(1, %s)
         """
        return self._execute_modify(sql, (n,))


    def generate_materials(self, n):
        sql = """
        INSERT INTO material(name, price_per_unit, unit)
        SELECT
          chr((65 + floor(random()*26))::int) ||
          chr((65 + floor(random()*26))::int),
          (random()*100+1)::int,
            'kg'
        FROM generate_series(1, %s)
          """
        return self._execute_modify(sql, (n,))


    def generate_consumations(self, n):
        product_ids = [p[0] for p in self._execute_select('SELECT id FROM "Product"')]
        material_ids = [m[0] for m in self._execute_select('SELECT id FROM material')]

        if not product_ids or not material_ids:
            print("[ERROR] Need at least 1 product and 1 material")
            return 0

        sql = """
        WITH params AS (
            SELECT %s::int[] AS pids, %s::int[] AS mids, %s::int AS n
        )
        INSERT INTO "Consumation"(product1_id, material_id, quatity)
        SELECT
            params.pids[floor(random()*array_length(params.pids,1))::int + 1],
            params.mids[floor(random()*array_length(params.mids,1))::int + 1],
            (random()*20+1)::int
        FROM params, generate_series(1, params.n)
        """

        return self._execute_modify(sql, (product_ids, material_ids, n))
