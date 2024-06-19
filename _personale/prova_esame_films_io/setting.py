# importa il modulo  os 
# che fornisce funzionalità per interagire con il sistema operativo. ###
import os

# Questa riga definisce la variabile  BASE_DIR 
# che contiene il percorso assoluto della directory corrente in cui si trova il file Python
# in esecuzione
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#  Questa riga definisce la variabile  DATABASE , 
# che contiene il percorso assoluto al file del database SQLite denominato 'db.sqlite3' 
# all'interno della directory 'database' situata nella directory corrente.
DATABASE = os.path.join(BASE_DIR, 'database', 'db.sqlite3')

#  Questa riga definisce la variabile  USER_TABLE_CSV , 
# che contiene il percorso assoluto al file CSV per la tabella degli utenti denominato 'users.csv'
# all'interno della directory 'database'. 
USER_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'users.csv')

# Questa riga definisce la variabile  FILM_TABLE_CSV ,
# che contiene il percorso assoluto al file CSV per la tabella dei film denominato 'films.csv'
# all'interno della directory 'database'. 
FILM_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'films.csv')

# Questa riga definisce la variabile  USER_TABLE_NAME  
# con il nome della tabella degli utenti come 'user'. 
USER_TABLE_NAME = 'user'

# Questa riga definisce la variabile  FILM_TABLE_NAME 
# con il nome della tabella dei film come 'film'.
FILM_TABLE_NAME = 'film'
