import os

# Percorso assoluto di dove ci troviamo noi
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Percorso assoluto al file del database SQLite
DATABASE = os.path.join(BASE_DIR, 'database', 'db.sqlite3')

# Percorsi assoluti ai file json per le tabelle
USERS_TABLE_JSON = os.path.join(BASE_DIR, 'database', 'users.json')
PRODUTTORI_TABLE_JSON = os.path.join(BASE_DIR, 'database', 'produttori.json')
PRODOTTI_TABLE_JSON = os.path.join(BASE_DIR, 'database', 'prodotti.json')
LOTTI_TABLE_JSON = os.path.join(BASE_DIR, 'database', 'lotti.json')
PRENOTAZIONI_TABLE_JSON = os.path.join(BASE_DIR, 'database', 'prenotazioni.json')

# Nomi delle tabelle
USERS_TABLE_NAME = 'user'
PRODUTTORI_TABLE_NAME = 'produttore'
PRODOTTI_TABLE_NAME = 'prodotto'
LOTTI_TABLE_NAME = 'lotto'
PRENOTAZIONI_TABLE_NAME = 'prenotazione'