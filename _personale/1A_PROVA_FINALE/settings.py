import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, 'db.sqlite3')

DATA_PATH = os.path.join(BASE_DIR, 'database', 'data_json')