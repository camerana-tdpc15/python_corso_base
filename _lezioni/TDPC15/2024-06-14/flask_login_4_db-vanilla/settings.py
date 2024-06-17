import os

# Ottiene il percorso assoluto alla cartella che contiene questo file,
# perché se si usano i percorsi realtivi, lanciando il programma con il "Run"
# di Visual Studio Code, la Current Working Directory (CWD) è la cartella del
# workspace, non quella in cui è contenuto il file app.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Percorso assoluto al file del database SQLite
DATABASE = os.path.join(BASE_DIR, 'database', 'db.sqlite3')

# Percorso assoluto al file CSV per la tabelle utenti
USER_TABLE_CSV = os.path.join(BASE_DIR, 'database', 'users.csv')

# Nome della tabella
USER_TABLE_NAME = 'user'
