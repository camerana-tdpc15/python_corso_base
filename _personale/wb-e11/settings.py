import os

#dichiariamo dove si trova la nostra app
BASE_DIR= os.path.abspath(os.path.dirname(__file__))

# uniamo in un percorso assoluto il file nostro al database sqlite
DATABASE= os.path.join(BASE_DIR,'database','db.sqlite3')

#percorsi assoluti ai file csv delle tabele utilizate
LOTTI_TABLE_CSV= os.path.join(BASE_DIR,'database','data_csv','lotti.csv')

PRENOTAZONI_TABLE_CSV= os.path.join(BASE_DIR,'database','data_csv','prenotazioni.csv')

PRODOTTI_TABLE_CSV= os.path.join(BASE_DIR,'database','data_csv','prodotti.csv')

PRODUTTORI_TABLE_CSV= os.path.join(BASE_DIR,'database','data_csv','produttori.csv')

USERS_TABLE_CSV= os.path.join(BASE_DIR,'database','data_csv','users.csv')



# Nomi delle tabelle

LOTTI_TABLE_NAME = 'lotti'
PRENOTAZONI_TABLE_NAME= 'prenotazioni'
PRODOTTI_TABLE_NAME = 'prodotti'
PRODUTTORI_TABLE_NAME = 'produttori'
USERS_TABLE_NAME = 'users'