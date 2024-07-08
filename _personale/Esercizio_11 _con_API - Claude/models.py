from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    ruolo = db.Column(db.String(10), default='user')
    prenotazioni = db.relationship("Prenotazione", back_populates="utente")

    serialize_rules = ('-password', '-prenotazioni.utente')

class Produttore(db.Model, SerializerMixin):
    __tablename__ = 'produttore'
    id = db.Column(db.Integer, primary_key=True)
    nome_produttore = db.Column(db.String(150), nullable=False)
    descrizione = db.Column(db.String(250))
    indirizzo = db.Column(db.String(250))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(150))
    prodotti = db.relationship("Prodotto", back_populates="produttore")

    serialize_rules = ('-prodotti.produttore',)

class Prodotto(db.Model, SerializerMixin):
    __tablename__ = 'prodotto'
    id = db.Column(db.Integer, primary_key=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey("produttore.id"), nullable=False)
    nome_prodotto = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(255))
    produttore = db.relationship("Produttore", back_populates="prodotti")
    lotti = db.relationship("Lotto", back_populates="prodotto")

    serialize_rules = ('-produttore.prodotti', '-lotti.prodotto')

class Lotto(db.Model, SerializerMixin):
    __tablename__ = 'lotto'
    id = db.Column(db.Integer, primary_key=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey("prodotto.id"), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean)
    prodotto = db.relationship("Prodotto", back_populates="lotti")
    prenotazioni = db.relationship("Prenotazione", back_populates="lotto")

    serialize_rules = ('-prodotto.lotti', '-prenotazioni.lotto')

class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazione'
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lotto_id = db.Column(db.Integer, db.ForeignKey("lotto.id"), nullable=False)
    qta = db.Column(db.Integer, nullable=False)
    utente = db.relationship("User", back_populates="prenotazioni")
    lotto = db.relationship("Lotto", back_populates="prenotazioni")

    serialize_rules = ('-utente.prenotazioni', '-lotto.prenotazioni')

def init_db(app):
    with app.app_context():
        db.create_all()