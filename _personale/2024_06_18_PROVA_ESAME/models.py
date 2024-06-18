# Importa la classe SQLAlchemy dal modulo Flask-SQLAlchemy. 
from flask_sqlalchemy import SQLAlchemy
from settings import USER_TABLE_NAME
from settings import FILM_TABLE_NAME

#  Crea un'istanza di SQLAlchemy per gestire le operazioni di database.
db = SQLAlchemy()

# DEVO DEFINIRE LE TABELLE USER
class User(db.Model):
    __tablename__ = USER_TABLE_NAME
    id = db.Column(db.Integer, primary_key = True )
    login = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.string(80), nullable = False)
    nome = db.Column(db.string(80))
    cognome = db.Column(db.string(80))
    indirizzo = db.Column(db.string)
    citta = db.Column(db.string(80))
    tel1 = db.Column(db.string(80))
    tel2 = db.Column(db.string(80))
    email = db.Column(db.string(80))
    data_nascita = db.Column(db.Date)
    data_reg = db.Column(db.Date)

    # DEVO DEFINIRE LE TABELLE FILM
class Film(db.Model):
    __tablename__ = FILM_TABLE_NAME
    id = db.Column(db.Integer, primary_key = True )
    title = db.Column(db.string(80))
    image = db.Column(db.string(80))



# Definisce una funzione chiamata 'init_db'
#  che accetta un parametro 'app'
# che rappresenta l'applicazione Flask corrente. 
def init_db(app):
    """
    Funzione per inizializzare il database e popolare le tabelle con i dati
    presenti nei file CSV.
    :param app: Applicazione Flask corrente (per accedere al logger)
    """

    # Questo metodo crea le tabelle nel database se non esistono già. 
    # Viene chiamato per inizializzare il database e creare 
    # le tabelle necessarie per l'applicazione. 
    db.create_all()

    if 


    