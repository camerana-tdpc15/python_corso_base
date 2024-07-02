import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Percorso assoluto al file del database SQLite
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'db.sqlite3')

# Percorsi assoluti ai file CSV per le tabelle utenti e film
USER_TABLE_CSV = os.path.join(BASE_DIR, 'data/data_csv', 'users.csv')
PRODUTTORI_TABLE_CSV = os.path.join(BASE_DIR, 'data/data_csv', 'produttori.csv')
PRODOTTI_TABLE_CSV = os.path.join(BASE_DIR, "data/data_csv","prodotti.csv")
PRENOTAZIONI_TABLE_CSV = os.path.join(BASE_DIR, "data/data_csv","prenotazioni.csv")
LOTTI_TABLE_CSV = os.path.join(BASE_DIR, "data/data_csv","lotti.csv")

# Nomi delle tabelle
USER_TABLE_NAME ="users"
PRODUTTORI_TABLE_NAME="produttori"
PRODOTTI_TABLE_NAME="prodotti"
PRENOTAZIONI_TABLE_NAME="prenotazioni"
LOTTI_TABLE_NAME="lotti"