#import mysql.connector

from providers import orders

class DatabaseService:
    def getGrid(self):
        return orders.grid_config

    def getOrders(self):
        return orders.order_wave

