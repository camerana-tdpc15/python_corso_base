import os

# Percorso assoluto di dove ci troviamo noi
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Percorso assoluto al file del database SQLite
DATABASE = os.path.join(BASE_DIR, 'database', 'db.sqlite3')

# Percorsi assoluti ai file CSV per le tabelle
USERS_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'users.csv')
PRODUTTORI_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'produttori.csv')
PRODOTTI_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'prodotti.csv')
LOTTI_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'lotti.csv')
PRENOTAZIONI_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'prenotazioni.csv')

# Nomi delle tabelle
USERS_TABLE_NAME = 'user'
PRODUTTORI_TABLE_NAME = 'produttore'
PRODOTTI_TABLE_NAME = 'prodotto'
LOTTI_TABLE_NAME = 'lotto'
PRENOTAZIONI_TABLE_NAME = 'prenotazione'