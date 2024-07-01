import os
# Definire la cartella generale di tutti i file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR,"database","db.sqlite3")

CONCERTO_TABLE_CSV = os.path.join(BASE_DIR, "database","Concerti.csv")
ORCHESTRA_TABLE_CSV = os.path.join(BASE_DIR, "database","Orchestre.csv")
SALA_TABLE_CSV = os.path.join(BASE_DIR, "database","Sale.csv")

CONCERTO_TABLE_NAME ="Concerto"
ORCHESTRA_TABLE_NAME="Orchestra"
SALE_TABLE_NAME="Sala"