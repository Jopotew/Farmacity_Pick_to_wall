
from providers.keys import db_keys as db
class DbKeys:
    def __init__(self, host, port, password, user, database):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.database = database

keys = DbKeys(db.database, db.user, db.password, db.port, db.host)