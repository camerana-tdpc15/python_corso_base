
import logging
import csv
import os
import sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from settings import USER_TABLE_CSV, PRODUTTORI_TABLE_CSV, PRODOTTI_TABLE_CSV, PRENOTAZIONI_TABLE_CSV, LOTTI_TABLE_CSV, USER_TABLE_NAME, PRODUTTORI_TABLE_NAME, PRODOTTI_TABLE_NAME, PRENOTAZIONI_TABLE_NAME, LOTTI_TABLE_NAME


db = SQLAlchemy()  # Crea l'istanza di SQLAlchemy


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
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

def init_db(app):
    # crea le tabelle se non esestono gia'
    db.create_all()

    #  popolo le tabelle .....

    if not User.query.first():
        if os.path.exists(USER_TABLE_CSV):
            with open(USER_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    new_record = User(
                       cognome = row["cognome"],
                       nome = row["nome"],
                       telefono = row["telefono"],
                       email = row["email"], 
                       password = row["password"] 
                    )
                    db.session.add(new_record)
                #modifiche si propagano sul db
                db.session.commit()
                app.logger.info(f"Tabella {USER_TABLE_CSV} è stata popolata")    
        else:
            app.logger.info(f"File {USER_TABLE_CSV} non esiste")
            sys.exit(1)    
    else:
        app.logger.info(f"Tabella {USER_TABLE_CSV} già popolata.")
        

   