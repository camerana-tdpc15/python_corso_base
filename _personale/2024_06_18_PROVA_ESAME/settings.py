#  Importa il modulo  os  che fornisce funzionalità per 
# interagire con il sistema operativo. 
import os

# Definisce una variabile  BASE_DIR  che contiene il percorso assoluto 
# alla directory del file corrente in cui si trova il codice sorgente. 
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Definisce una variabile  DATABASE  che contiene il percorso assoluto al file 
# del database SQLite. 
# Viene creato un percorso combinando  BASE_DIR  con la directory 'database' 
# e il nome del file 'db.sqlite3'. 
DATABASE = os.path.join(BASE_DIR, 'database', 'db.sqlite3')

#  Definisce una variabile  USER_TABLE_CSV  che contiene il percorso assoluto 
# al file CSV per la tabella degli utenti. 
# Viene creato un percorso simile a quello del database. 
USER_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'users.csv')

# Definisce una variabile  FILM_TABLE_CSV  che contiene il percorso assoluto 
# al file CSV per la tabella dei film. 
# Anche qui viene creato un percorso simile a quello del database. 
FILM_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'films.csv')

# Definiscono le variabili Nomi delle tabelle
USER_TABLE_NAME = 'user'
FILM_TABLE_NAME = 'film'