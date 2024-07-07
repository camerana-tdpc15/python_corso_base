from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import app
from models import User, Produttore, Prodotto, Lotto, Prenotazione
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Produttore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produttore = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.String(255), nullable=False)
    indirizzo = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Prodotto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttore.id'), nullable=False)
    nome_prodotto = db.Column(db.String(100), nullable=False)
    produttore = db.relationship('Produttore', backref=db.backref('prodotti', lazy=True))

class Lotto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotto.id'), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, default=False)
    prodotto = db.relationship('Prodotto', backref=db.backref('lotti', lazy=True))

class Prenotazione(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotto.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)
    utente = db.relationship('User', backref=db.backref('prenotazioni', lazy=True))
    lotto = db.relationship('Lotto', backref=db.backref('prenotazioni', lazy=True))

def init_db():
    # Crea le tabelle solo se non esistono già
    

    # Popolo le tabelle con i dati se non esiste un record in User
    if User.query.first() is None:
        with app.app_context():
            db.create_all()

        # Popola il database con i dati iniziali
        with open('users.json') as f:
            users = json.load(f)
            for user in users:
                db.session.add(User(**user))
        
        with open('produttori.json') as f:
            produttori = json.load(f)
            for produttore in produttori:
                db.session.add(Produttore(**produttore))

        with open('prodotti.json') as f:
            prodotti = json.load(f)
            for prodotto in prodotti:
                db.session.add(Prodotto(**prodotto))
        
        with open('lotti.json') as f:
            lotti = json.load(f)
            for lotto in lotti:
                lotto['data_consegna'] = datetime.strptime(lotto['data_consegna'], '%Y-%m-%d').date()
                db.session.add(Lotto(**lotto))
        
        with open('prenotazioni.json') as f:
            prenotazioni = json.load(f)
            for prenotazione in prenotazioni:
                db.session.add(Prenotazione(**prenotazione))

        db.session.commit()
