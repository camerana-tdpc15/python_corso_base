import os

# percorso assoluto app
BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

#percorso database, dicendo che è uguale a BASE_DIR_PATH
DATABASE_PATH = os.path.join(BASE_DIR_PATH,'database','db.sqlite3')