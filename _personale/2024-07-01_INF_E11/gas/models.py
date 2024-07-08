import os
import json
from flask_sqlalchemy import SQLAlchemy
from settings import BASE_DIR


db = SQLAlchemy()

class User (db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50),nullable=False)
    telefono = db.Column(db.String)
    email = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(30),nullable=False)

class Produttore (db.Model):
    __tablename__= 'produttori'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produttore = db.Column(db.String(50),unique=True)
    descrizione = db.Column(db.Text(50),nullable=False)
    indirizzo = db.Column(db.Text(),nullable=False)
    telefono = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(30),nullable=False)


class Prodotto (db.Model):
    __tablename__= 'prodotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produttore_id = db.Column(db.Integer,db.ForeignKey('produttori.id'),nullable=False)
    nome_prodotto = db.Column(db.String(50),nullable=False)
     # RELATIONSHIPS
    rel_lotti =  db.relationship('lotto', back_populates='rel_prodotto')

class Lotto (db.Model):
    __tablename__= 'lotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodotto_id = db.Column(db.Integer,db.ForeignKey('prodotti.id'),nullable=False)
    data_consegna=db.Column(db.String)
    qta_unita_misura = db.Column(db.String(10),nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False )
    sospeso = db.Column(db.Boolean, default=False)
    # RELATIONSHIPS
    rel_prodotto = db.relationship('Prodotto', back_populates='rel_lotti')
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_lotti')

    serialize_rules = ('-rel_prodotto.rel_lotti', 'get_date','get_prezzo_str', 'get_qta_disponibile' )

    def get_date(self):# Quando siamo in una classe e definiamo una funzione
        res_data = self.data_consegna.strftime('%A %d/%m/%Y')
        return res_data
        
    def get_prezzo_str(self):
        return f'{self.prezzo_unitario} €/{self.qta_unita_misura}'
    
    def get_qta_disponibile(self):
        qta_prenotata = 0
        for prenot in self.rel_prenotazioni:
            qta_prenotata += prenot.qta

            return self.qta_lotto - qta_prenotata

class Prenotazione (db.Model):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    # RELATIONSHIP
    rel_prodotto = db.relationship('Lotto', back_populates='rel_prenotazioni')
    

def init_db(app):
   # crea le tabelle se non esistono già
    db.create_all()

            
            
