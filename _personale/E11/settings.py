import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE  = os.path.join(BASE_DIR,'database','db.sqlite3')



# Percorsi assoluti ai file CSV per le tabelle 
USERS_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'users.csv')
LOTTI_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'lotti.csv')
PRENOTAZIONI_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'prenotazioni.csv')
PRODOTTI_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'prodotti.csv')
PRODUTTORI_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'produttori.csv')

