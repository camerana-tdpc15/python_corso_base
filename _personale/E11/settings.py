import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_PATH  = os.path.join(BASE_DIR,'database','db.sqlite3')

USERS_FILE_PATH = os.path.join(BASE_DIR,'database', 'users.csv') 
PRENOTAZIONI_FILE_PATH = os.path.join(BASE_DIR,'database', 'prenotazioni.csv') 
PRODOTTI_FILE_PATH = os.path.join(BASE_DIR,'database', 'prodotti.csv') 
PRODUTTORI_FILE_PATH = os.path.join(BASE_DIR,'database', 'produttori.csv') 
LOTTI_FILE_PATH = os.path.join(BASE_DIR,'database', 'lotti.csv') 