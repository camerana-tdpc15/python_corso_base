from  flask_sqlalchemy import SQLAlchemy
from settings_esercizio07 import USER_TABLE_NAME, USER_TABLE_CSV,FILM_TABLE_NAME, USER_TABLE_CSV





db = SQLAlchemy()

#   DEFINIRE LE TABELE
class User(db.Model):
    __tablename__ = USER_TABLE_NAME  # il nome e definito in settings...
    id = db.Column(db.Integre, primary_key=True)
    login = db.Column(db.String(80), unique = True, nullable = False)
    password = db.collumn(db.String(80), nullable = False)
    nome = db.Column(db.string(80))
    cognome = db.Column(db.String(80))
    indirizzo = db.Column(db.String(120))
    citta = db.Column(db.String(80))
    tel_01 = db.Column(db.String(20))
    tel_02 = db.Column(db.String(20))
    email = db.Column(db.String(80))
    data_nascita = db.Column(db.Date)
    data_registrazione = db.Column(db.Data)




class Film(db.Model):
    __tablename__ = FILM_TABLE_NAME  # il nome e definito in settings...
    id = db.Column(db.Integer, primary_key=True)    #colonna chiamata id 
    #tipo di dato intero,impostata come chiave primaria per la tabella
    title = db.Column(db.String(80), nullable=False)    #colonna chiamata title  
    # tipo di dato stringa (di lunghezza massima 80 caratteri) e la rende non nulla (nullable=False).
    # Questo significa che ogni riga nella tabella deve avere un valore per la colonna title
    image = db.Column(db.String(80), nullable=False)



    


def init_db(app):

    db.create_all()

    # PER OGNI TABELA IMPORTARE I DATI
    #se c'e un record si/no
    #se si_non devo fare nulla
    #se no:
        #cercare csv, se lo trovi
