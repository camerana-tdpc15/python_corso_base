import os
from flask import Flask, render_template, request, session, redirect, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name_user = db.Column(db.String, nullable=False)
    first_name_user = db.Column(db.String, nullable=False)
    telephon_number_user = db.Column(db.Integer)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    # messaggi = db.relationship('Messaggio', backref=db.backref('utente'))
    # --- OR ---
    

class Produttore(db.Model):
    __tablename__ = 'produttori'
    id = db.Column(db.Integer, primary_key=True)
    first_name_produt = db.Column(db.String, nullable=False)
    descrizione = db.Column(db.Text)
    indirizzo = db.Column(db.Text, nullable=False)
    telephon_number_produt = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    
    class prodotto_prenotabile(db.Model):
     __tablename__ = 'prodotti prenotabili'
    id = db.Column(db.Integer, primary_key=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), nullable=False)
    name_prodotto = db.Column(db.String, nullable=False)
    
    class lotto(db.Model):
     __tablename__ = 'lotti'
    id = db.Column(db.Integer, primary_key=True)
    prodotto_prenotabile_id = db.Column(db.Integer, db.ForeignKey('prodotti_prenotabili.id'), nullable=False)
    data_consegna = db.Column(db.DateTime, nullable=False)
    qta_unita_misura = db.Column(db.Integer, nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, nullable=False)
    
    class prenotazione(db.Model)
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)
    user_id = db.column(db.Inetegr, db.ForeignKey('users.id'), nullable=False)
    qta = db.Column(db.Ineger, nullable=False)
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)