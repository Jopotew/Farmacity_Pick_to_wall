import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

import pymysql
from models.grid_config_model import GridConfig
from models.order_model import Order
from models.item_model import Item
from models.bd_keys_model import keys

# from providers import orders


class DatabaseService:
    """
    A service class responsible for interacting with a MySQL database to retrieve and
    manipulate order and grid data.

    This class handles database connections, executes SQL queries, and returns results
    mapped to appropriate model objects.

    Attributes:
        cursor: A pymysql cursor object used to execute queries.
        connection: A pymysql connection object used to connect to the MySQL database.

    Methods:
        __init__(self):
            Initializes the database connection and cursor.

        getGrid(self) -> GridConfig:
            Retrieves grid configuration data from the database.

        getOrders(self, grid_positions: int) -> list[Order]:
            Retrieves a list of orders and their related items from the database.

        change_order_status(self, status):
            A placeholder method to change the status of an order (not implemented).
    """

    def __init__(self):
        """
        Initializes the connection to the MySQL database using pymysql.

        Creates a connection to the database and prepares a cursor for executing SQL queries.
        If the connection or cursor cannot be established, it prints an error message.
        """
        self.cursor = None
        self.connection = None
        
        try:

            self.connection = pymysql.connect(
                host="localhost",  # Dirección del servidor
                user="root",  # Usuario
                password="Farmacity2024",  # Contraseña
                database="trabajofarmacity",  # Nombre de la base de datos
                cursorclass=pymysql.cursors.DictCursor,
                port=3306,
            )

            self.cursor = self.connection.cursor()

        except pymysql.MySQLError as e:
            print(f"Error al conectar con MySQL: {e}")

        finally:

            if self.connection and not self.connection.open:
                self.cursor.close()
                self.connection.close()

    def getGrid(self) -> GridConfig:
        """
        Retrieves the grid configuration from the database.

        Executes a SQL query to fetch the grid row and column configuration.

        Returns:
            GridConfig: An object representing the grid configuration.
        """
        consulta = "SELECT gridrow, gridcol FROM grid;"
        print(consulta)
        self.cursor.execute(consulta)
        resultado = self.cursor.fetchall()
        return GridConfig.fromDict(resultado[0])

    def getOrders(self, grid_positions: int) -> list[Order]:
        """
        Retrieves a limited number of orders and their related items from the database.

        This method fetches orders assigned to the grid positions and their associated items,
        while ensuring that only orders with a valid status (id_status = 1) are included.

        Args:
            grid_positions (int): The maximum number of orders to retrieve.

        Returns:
            list[Order]: A list of Order objects, each containing related Item objects.
        """
        try:

            consulta_orders = """
            SELECT id_order_assign 
            FROM order_assign
            WHERE id_status = 1
            LIMIT %s;
            """
            self.cursor.execute(consulta_orders, (grid_positions))
            orders = self.cursor.fetchall()

            if not orders:
                print("No hay órdenes disponibles.")
                return []

            order_wave = []

            for order in orders:
                id_order_assign = order["id_order_assign"]
                consulta_items = """
                SELECT i.farma_id, i.item_name, i.bar_code
                FROM order_wave ow
                INNER JOIN items i ON ow.id_item = i.id_item
                WHERE ow.id_order_assign = %s;
                """
                self.cursor.execute(consulta_items, (id_order_assign,))
                items = self.cursor.fetchall()

                order = Order(
                    items=list(map(Item.fromDict, items)), order_id=id_order_assign
                )
                order_wave.append(order)

            return order_wave

        except pymysql.MySQLError as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

    def change_order_status(self, id_order_assign: int, status: int):
        """
        Changes the status of an order in the database.

        This method updates the `id_status` of a specific order in the `order_assign` table.

        Args:
            id_order_assign (int): The ID of the order to update.
            status (int): The new status of the order (2 for packing, 3 for dispatch).

        Returns:
            bool: True if the status was successfully updated, False otherwise.
        """
        try:
            # Verificar que el estado esté entre los valores válidos (2 o 3)
            if status not in [2, 3]:
                print(
                    "Estado no válido. El estado debe ser 2 (empaquetado) o 3 (despacho)."
                )
                return False

            consulta_update_status = """
            UPDATE order_assign
            SET id_status = %s
            WHERE id_order_assign = %s;
            """
            self.cursor.execute(consulta_update_status, (status, id_order_assign))

            self.connection.commit()

            if self.cursor.rowcount > 0:
                print(
                    f"El estado de la orden {id_order_assign} ha sido actualizado a {status}."
                )
                return True
            else:
                print(f"No se encontró la orden con ID {id_order_assign}.")
                return False

        except pymysql.MySQLError as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False
