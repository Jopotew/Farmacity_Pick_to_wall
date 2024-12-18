import mysql.connector

from led import data

class DatabaseService:
    def getGrid(self):
        return data.grid_config

    def getOrders(self):
        return data.order_wave

