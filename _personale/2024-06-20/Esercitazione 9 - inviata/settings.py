import os

BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR_PATH, 'db.sqlite3')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SECRET_KEY = 'mysecretkey'

# Nomi delle tabelle
UTENTI_TABLE = 'utenti'
MESSAGGI_TABLE = 'messaggi'