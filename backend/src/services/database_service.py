import sys
import os
import pymysql
from models.grid_config_model import GridConfig
from models.order_model import Order
from models.item_model import Item
from models.bd_keys_model import keys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)

class DatabaseService:
    """
    A service class responsible for interacting with a MySQL database to retrieve and
    manipulate order and grid data.

    Attributes:
        cursor: A pymysql cursor object used to execute queries.
        connection: A pymysql connection object used to connect to the MySQL database.
    """

    def __init__(self):
        """
        Initializes the connection to the MySQL database using pymysql.

        Creates a connection to the database and prepares a cursor for executing SQL queries.
        """
        self.cursor = None
        self.connection = None

        try:
            self.connection = pymysql.connect(
                host="localhost",
                user="root",
                password="Farmacity2024",
                database="trabajofarmacity",
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

    def get_grid(self) -> GridConfig:
        """
        Retrieves the grid configuration from the database.

        Returns:
            GridConfig: An object representing the grid configuration.
        """
        query = "SELECT gridrow, gridcol FROM grid;"
        print(query)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return GridConfig.fromDict(result[0])

    def get_orders(self, grid_positions: int) -> list[Order]:
        """
        Retrieves a limited number of orders and their related items from the database.

        Args:
            grid_positions (int): The maximum number of orders to retrieve.

        Returns:
            list[Order]: A list of Order objects, each containing related Item objects.
        """
        try:
            query_orders = """
            SELECT id_order_assign 
            FROM order_assign
            WHERE id_status = 1
            LIMIT %s;
            """
            self.cursor.execute(query_orders, (grid_positions,))
            orders = self.cursor.fetchall()

            if not orders:
                print("No hay órdenes disponibles.")
                return []

            order_wave = []

            for order in orders:
                order_assign_id = order["id_order_assign"]
                query_items = """
                SELECT i.id_item, i.farma_id, i.item_name, i.bar_code
                FROM order_wave ow
                INNER JOIN items i ON ow.id_item = i.id_item
                WHERE ow.id_order_assign = %s;
                """
                self.cursor.execute(query_items, (order_assign_id,))
                items = self.cursor.fetchall()

                order_obj = Order(
                    items=list(map(Item.fromDict, items)), order_id=order_assign_id
                )
                order_wave.append(order_obj)

            return order_wave

        except pymysql.MySQLError as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []

    def change_order_status(self, order_assign_id: int, status: int):
        """
        Changes the status of an order in the database.

        Args:
            order_assign_id (int): The ID of the order to update.
            status (int): The new status of the order (2 for packing, 3 for dispatch).

        Returns:
            bool: True if the status was successfully updated, False otherwise.
        """
        try:
            if status not in [2, 3]:
                print("Estado no válido. El estado debe ser 2 (empaquetado) o 3 (despacho).")
                return False

            query_update_status = """
            UPDATE order_assign
            SET id_status = %s
            WHERE id_order_assign = %s;
            """
            self.cursor.execute(query_update_status, (status, order_assign_id))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                print(f"El estado de la orden {order_assign_id} ha sido actualizado a {status}.")
                return True
            else:
                print(f"No se encontró la orden con ID {order_assign_id}.")
                return False

        except pymysql.MySQLError as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False

    def set_item_status(self, order_assign_id: int, item_id: int) -> bool:
        """
        Marks an item as selected in the order_wave table for a specific order_assign.

        Args:
            order_assign_id (int): The ID of the assigned order.
            item_id (int): The ID of the item.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            query_update_item_status = """
            UPDATE order_wave
            SET id_item_status = TRUE
            WHERE id_order_assign = %s AND id_item = %s;
            """
            self.cursor.execute(query_update_item_status, (order_assign_id, item_id))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                print(f"El item {item_id} de la orden {order_assign_id} fue marcado como seleccionado.")
                return True
            else:
                print(f"No se encontró el item {item_id} en la orden {order_assign_id}.")
                return False

        except pymysql.MySQLError as e:
            print(f"Error al actualizar el estado del item: {e}")
            return False

    def update_order_position(self, order_assign_id: int, position: int) -> bool:
        """
        Assigns a position to all orders with the same id_order_assign if they are in preparation.

        Args:
            order_assign_id (int): The ID of the assigned order.
            position (int): The position to assign to the order.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            query_check_status = """
            SELECT id_status
            FROM order_assign
            WHERE id_order_assign = %s;
            """
            self.cursor.execute(query_check_status, (order_assign_id,))
            result = self.cursor.fetchone()

            if not result or result['id_status'] != 1:
                print(f"La orden {order_assign_id} no está en preparación y no puede ser actualizada.")
                return False

            query_update_position = """
            UPDATE order_position
            SET position = %s
            WHERE id_order_assign = %s;
            """
            self.cursor.execute(query_update_position, (position, order_assign_id))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                print(f"La posición {position} fue asignada a la orden {order_assign_id}.")
                return True
            else:
                print(f"No se pudo asignar una posición a la orden {order_assign_id}.")
                return False

        except pymysql.MySQLError as e:
            print(f"Error al actualizar la posición de la orden: {e}")
            return False
