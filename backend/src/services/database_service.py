import mysql.connector

# from providers import orders


class DatabaseService:

    def __init__(self):
        self.cursor = None
        self.connection = None
        try:

            self.connection = mysql.connector.connect(
                host="localhost",  # Dirección del servidor
                user="root",  # Usuario
                password="Jopotew22!",  # Contraseña
                database="farmacity_pw",  # Nombre de la base de datos
            )

            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)

        except mysql.connector.Error as e:
            print(f"Error al conectar con MySQL: {e}")

        finally:
            if "connection" in locals() and self.connection.is_connected():
                self.cursor.close()
                self.connection.close()

    def getGrid(self):
        consulta = "SELECT gridrow, gridcol FROM grid;"
        self.cursor.execute(consulta)
        resultado = self.cursor.fetchall()
        return resultado[0]

    def getOrders(self, grid_positions: int):
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
                return {}

            order_wave = {}

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
                order_wave[id_order_assign] = items
            return order_wave

        except mysql.connector.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return {}
