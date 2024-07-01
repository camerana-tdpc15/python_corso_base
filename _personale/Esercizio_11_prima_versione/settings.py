import os

# Percorso assoluto di dove ci troviamo noi
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Percorso assoluto al file del database SQLite
DATABASE = os.path.join(BASE_DIR, 'database', 'db.sqlite3')

# Percorsi assoluti ai file CSV per le tabelle
USER_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'users.csv')
PRODUTTORE_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'produttori.csv')
PRODOTTO_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'prodotti.csv')
LOTTO_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'lotti.csv')
PRENOTAZIONE_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'prenotazioni.csv')

# Nomi delle tabelle
USER_TABLE_NAME = 'user'
PRODUTTORE_TABLE_NAME = 'produttore'
PRODOTTO_TABLE_NAME = 'prodotto'
LOTTO_TABLE_NAME = 'lotto'
PRENOTAZIONE_TABLE_NAME = 'prenotazione'