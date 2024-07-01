import os

# ottengo il percorso assoluto dal file app.py che è la nostra app
BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

# trovo l'indirizzo del database, dicendo che il percorso è uguale a BASE_DIR_PATH, nella cartella database
DATABASE_PATH = os.path.join(BASE_DIR_PATH, 'database','db.sqlite3')