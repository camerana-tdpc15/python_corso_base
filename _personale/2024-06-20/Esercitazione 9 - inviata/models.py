from flask_sqlalchemy import SQLAlchemy
from settings import UTENTI_TABLE, MESSAGGI_TABLE

db = SQLAlchemy()

class Utente(db.Model):
    __tablename__ = UTENTI_TABLE
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    messaggi = db.relationship('Messaggio', back_populates='utente')

class Messaggio(db.Model):
    __tablename__ = MESSAGGI_TABLE
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{UTENTI_TABLE}.id'), nullable=False)
    messaggio = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    utente = db.relationship('Utente', back_populates='messaggi')