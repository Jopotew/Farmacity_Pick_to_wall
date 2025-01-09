import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)




import pymysql
from models.grid_config_model import GridConfig
from models.order_model import Order
from models.item_model import Item

# from providers import orders


class DatabaseService:

    def __init__(self):
        self.cursor = None
        self.connection = None
        try:
            # Conexión a la base de datos usando pymysql
            self.connection = pymysql.connect(
                host="localhost",  # Dirección del servidor
                user="ljuan",  # Usuario
                password="Farmacity2024",  # Contraseña
                database="trabajofarmacity",  # Nombre de la base de datos
                cursorclass=pymysql.cursors.DictCursor,  # Para obtener los resultados como diccionario
                port=3306
            )

            # Intentamos crear el cursor solo si la conexión es exitosa
            self.cursor = self.connection.cursor()

        except pymysql.MySQLError as e:
            print(f"Error al conectar con MySQL: {e}")

        finally:
            # Aseguramos el cierre adecuado de la conexión y el cursor
            if self.connection and not self.connection.open:
                self.cursor.close()
                self.connection.close()

    def getGrid(self) -> GridConfig:
        consulta = "SELECT gridrow, gridcol FROM grid;"
        self.cursor.execute(consulta)
        resultado = self.cursor.fetchall()
        return GridConfig.fromDict(resultado[0])

    def getOrders(self, grid_positions: int) -> list[Order]:
        """
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Obtiene una cantidad limitada de órdenes asignadas y los items relacionados.
        :param grid_positions: Número máximo de órdenes a recuperar.
        :return: Diccionario con los datos de las órdenes y sus items.
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """

        try:
            consulta_orders = """
            SELECT id_order_assign 
            FROM order_assign
            LIMIT %s;
            """
            self.cursor.execute(consulta_orders, (grid_positions,))
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
                order = Order(items=map(Item.fromDict, items))
                order_wave.append(order)

            return order_wave

        except pymysql.MySQLError as e:
            print(f"Error al ejecutar la consulta: {e}")
            return []
