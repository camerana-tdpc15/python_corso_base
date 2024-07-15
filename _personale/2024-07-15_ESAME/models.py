import os
import json
from datetime import date
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from settings import BASE_DIR

db = SQLAlchemy()

class Utente(db.Model, SerializerMixin):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    serialize_rules = ('-password',)

class Replica(db.Model, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventi.id'), nullable=False)
    data_ora = db.Column(db.Date, nullable=False)
    annullato = db.Column(db.Boolean, default=False)

class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)
    replica_id = db.Column(db.Integer, db.ForeignKey('repliche.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)
    # RELATIONSHIPS
    

class Locale(db.Model, SerializerMixin):
    __tablename__ = 'locali'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_locale = db.Column(db.String(50), nullable=False)
    luogo = db.Column(db.String(100), nullable=False)
    posti = db.Column(db.Integer, nullable=False)

class Evento(db.Model, SerializerMixin):
    __tablename__ = 'eventi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locale_id = db.Column(db.Integer, db.ForeignKey('locali.id'), nullable=False)
    nome_evento = db.Column(db.String(50), nullable=False)
   