import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Percorso assoluto al file del database SQLite
DATABASE = os.path.join(BASE_DIR, 'database', 'db.sqlite3')

# Percorsi assoluti ai file CSV per le tabelle utenti e film
USER_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'users.csv')
FILM_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'films.csv')

# Nomi delle tabelle
USER_TABLE_NAME = 'user'
FILM_TABLE_NAME = 'film'
