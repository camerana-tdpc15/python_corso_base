import os
# Definire la cartella generale di tutti i file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = os.path.join(BASE_DIR,"database","db.sqlite3")

STUDENTE_TABLE_CSV = os.path.join(BASE_DIR, "database","Studenti.csv")
CORSO_TABLE_CSV = os.path.join(BASE_DIR, "database","Corsi.csv")
DOCENTE_TABLE_CSV = os.path.join(BASE_DIR, "database","Docenti.csv")
ESAME_TABLE_CSV = os.path.join(BASE_DIR, "database","Esami.csv")

STUDENTE_TABLE_NAME ="Studente"
CORSO_TABLE_NAME="Corso"
DOCENTE_TABLE_NAME="Docente"
ESAME_TABLE_NAME="Esame"