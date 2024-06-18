import os
# Questo modulo consente di interagire con il sistema operativo del computer,
#  sia che tu stia lavorando su Windows, Linux o macOS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# BASE_DIR è una variabile che rappresenta il percorso assoluto della directory in cui si trova il file Python corrente.
# restituisce la cartella in cui si trova il file in cui hai scritto quella riga di codice

DATA_BASE = os.path.join(BASE_DIR, "db", "db.sqlite3")
# crea un percorso completo al file db.sqlite3 all’interno della cartella db all’interno della directory di base del tuo progetto.
# In altre parole, DATA_BASE conterrà il percorso completo al file del database.


# ESEMPIO DA IA
#import os

 # Esempio di percorsi
#directory = "progetto"
#sottocartella = "db"
#nome_file = "db.sqlite3"

 # Unisci i percorsi
#percorso_completo = os.path.join(directory, sottocartella, nome_file)

#print("Percorso completo:", percorso_completo)

USER_TABLE_CSV = os.path.join(BASE_DIR, "db", "user.css")
FILM_TABLE_CSV = os.path.join(BASE_DIR, "db", "films.csv")
# USER_TABBE_CSV conterrà il percorso completo al file user.csv all’interno della cartella db 
# all’interno della directory di base del tuo progetto.

USER_TABLE_NAME = "user"
FILM_TABLE_NAME = "films"
# hai definito la variabile USER_TABLE_NAME con il valore "user".
# Questo ti permetterà di utilizzare il nome della tabella in modo più flessibile nel tuo codice.

