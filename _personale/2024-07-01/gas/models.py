
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()  # Crea l'istanza di SQLAlchemy


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

class Produttore(db.Model):
    __tablename__ = 'produttori'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produttore = db.Column(db.String(100), unique=True, nullable=False)
    descrizione = db.Column(db.Text, nullable=False)
    indirizzo = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

class Prodotto(db.Model):
    __tablename__ = 'prodotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), unique=True, nullable=False)
    nome_prodotto = db.Column(db.String(50), nullable=False)
    
class Lotto(db.Model):
    __tablename__ = 'lotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, unique=True, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, default=False)

class Prenotazione(db.Model):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), unique=True, nullable=False)
    qta = db.Column(db.Integer, nullable=False)

def init_db():
    # crea le tabelle se non esestono gia'
    db.create_all()

    #  popolo le tabelle .....
        

   