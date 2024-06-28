import as
from flask_sqlalchemy import SQULAlchemy
from settings import USER_TABLE_NAME, FILM_TABLE_NAME

db = SQLAlchemy()

# DEFINIRE LE TABELLE
class user(db.Model):
    __tablename__ = USER_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    nome = db.Column(db.String(80))
    cognome = db.Column(db.String(80))
    indirizzo = db.Column(db.String(120))
    citta = db.Column(db.String(80))
    tel1 = db.Column(db.String(20))
    tel2 = db.Column(db.String(20))
    email = db.Column(db.String(100))
    data_nascita = db.Column(db.Date)
    data_reg = db.Column(db.Date)

    class film(db.Model):
        __tablename__ = FILM_TABLE_NAME
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80), nullable=False )
        image = db.Column(db.String, nullable=False)

def int_db(app):
     
    # Crea le tabelle nel database, se queste non esistono già
    db.create_all()

 if not User

    # IMPORTARE I DATI