import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "..")
sys.path.append(src_path)


from providers.keys import db_keys as db
class DbKeys:
    def __init__(self, host, port, password, user, database):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.database = database

keys = DbKeys(db.database, db.user, db.password, db.port, db.host)
