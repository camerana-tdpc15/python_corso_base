import os
import json
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from settings import BASE_DIR, DATABASE_PATH, DATA_PATH

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome= db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False) 

    prenotazioni = db.relationship('Prenotazione', back_populates='user', lazy='dynamic')

    serialize_rules = ('-prenotazioni.user', '-password')

class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    replica_id = db.Column(db.Integer, db.ForeignKey('repliche.id'), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)

     # -- RELATIONSHIPS --
    user = db.relationship('User', back_populates='prenotazioni')
    lotto = db.relationship('Replica', back_populates='prenotazioni')  

    serialize_rules = ('-user.prenotazioni', '-replica.prenotazioni') #/,'get_prezzo_totale_str'/#)

class Replica(db.Model, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventi.id'), nullable=False)
    data_ora = db.Column(db.DateTime, nullable=False)
    annullato = db.Column(db.Boolean, nullable=False)

class Evento(db.Model, SerializerMixin):
    __tablename__ = 'eventi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locale_id = db.Column(db.Integer, db.ForeignKey('locali.id'), nullable=False)
    nome_evento = db.Column(db.String(50), unique=True, nullable=False)

class Locale(db.Model, SerializerMixin):
    __tablename__ = 'locali'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_locale = db.Column(db.String(50), unique=True, nullable=False)
    luogo = db.Column(db.String(100), unique=True, nullable=False)
    posti = db.Column(db.Integer, autoincrement=True)
    

def init_db():
    db.create_all()

    if User.query.first() is None:
        json_files = [
            ('utenti.json', User),
            ('prenotazioni.json', Prenotazione ),
            ('repliche.json', Replica ),
            ('eventi.json', Evento ),
            ('locali.json', Locale ),
        ]

        for filename, model in json_files:
            filepath = os.path.join(DATA_PATH, filename)

            with open (filepath, 'r') as file:
                lista_record = json.load(file)

            for record_dict in lista_record:
                if 'data_ora' in record_dict:
                    var_data_ora = datetime.strptime(record_dict['data_ora'], '%d-%m-%Y-%H:%M:%S' )
                    record_dict['data_ora'] = var_data_ora
                    
                new_record = model(**record_dict)
                db.session.add(new_record)
        db.session.commit()



