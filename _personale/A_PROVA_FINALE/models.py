import os
import json
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from settings import BASE_DIR, DATA_PATH, DATABASE_PATH

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False) 

    serialize_rules = ('-password', '-prenotazioni.user')

    prenotazioni = db.relationship('Prenotazione', back_populates='user', lazy='dynamic')

class Produttore(db.Model, SerializerMixin):
    __tablename__ = 'produttori'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produttore = db.Column(db.String(100), unique=True, nullable=False)
    descrizione = db.Column(db.String(50), nullable=False)
    indirizzo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    prodotti = db.relationship('Prodotto', back_populates='produttore')

    serialize_rules = ('-prodotti.produttore', '-prodotti.lotti.prenotazioni')


   
   

class Prodotto(db.Model, SerializerMixin):
    __tablename__ = 'prodotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), nullable=False)
    nome_prodotto = db.Column(db.String(50), nullable=False)

    produttore = db.relationship('Produttore', back_populates='prodotti')
    lotti = db.relationship('Lotto', back_populates='prodotto')

class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='prenotazioni')
    lotto = db.relationship('Lotto', back_populates='prenotazioni')




class Lotto(db.Model, SerializerMixin):
    __tablename__ = 'lotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura= db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, nullable=False)

    prodotto = db.relationship('Prodotto', back_populates='lotti')
    prenotazioni = db.relationship('Prenotazione', back_populates='lotto')

    serialize_rules = ('-')


def init_db():
    
    db.create_all()
    
    if User.query.first() is None:
        json_files = [
            ('lotti.json', Lotto),
            ('prenotazioni.json', Prenotazione ),
            ('prodotti.json', Prodotto ),
            ('produttori.json', Produttore ),
            ('users.json', User ),
        ]

        for filename, model in json_files:
            filepath = os.path.join(DATA_PATH, filename)

            with open (filepath, 'r') as file:
                lista_record = json.load(file)

            for record_dict in lista_record:
                if 'data_consegna'in record_dict:
                    var_data_consegna = date.fromisoformat(record_dict['data_consegna'])
                    record_dict['data_consegna'] = var_data_consegna  
                
                new_record = model(**record_dict)
                db.session.add(new_record)
        db.session.commit()
            

        
        












