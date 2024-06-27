# INIZIO DA SETTING

# devo ottenere il path assoluto della cartella contenente tutti i file
import os
BASE_DIR    = os.path.abspath(os.path.dirname(__file__))

# devo definire il percorso del database
DATABASE = os.path.join(BASE_DIR, "database", "db.sqlite3")

# per importare le varie tabelle devo dire qual'è il percorso dei vari file 
CONCERTI_TABLE_CSV = os.path.join(BASE_DIR, "database", "Concerti.csv") 
ORCHESTRA_TABLE_CSV = os.path.join(BASE_DIR, "database", "Orchestra.csv") 
SALA_TABLE_CSV = os.path.join(BASE_DIR, "database", "Sale.csv")

# definisco i nomi delle tabelle
CONCERTO_TABLE_NAME = "Concerto"
ORCHESTRA_TABLE_NAME = "Orchestra"
SALA_TABLE_NAME = "Sala"

# ORA PASSO AL FILE MODELS!!!!