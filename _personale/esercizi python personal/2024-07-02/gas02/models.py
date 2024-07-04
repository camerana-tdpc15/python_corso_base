import os
import json
from datetime import date
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from settings import BASE_DIR

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

class Produttore(db.Model):
    __tablename__ = 'produttori'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produttore = db.Column(db.String(), unique=True, nullable=False)
    descrizione = db.Column(db.Text(), nullable=False)
    indirizzo = db.Column(db.Text(), nullable=False)
    telefono = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)

class Prodotto(db.Model):
    __tablename__ = 'prodotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), nullable=False)
    nome_prodotto = db.Column(db.String(50), nullable=False)

class Lotto(db.Model):
    __tablename__ = 'lotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, default=False)


class Prenotazione(db.Model):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)

    # @TODO: Da implementare l'unique constraint per la coppia lotto_id e user_id
    # ...

def init_db():
    # Crea le tabelle se non esistono già
    db.create_all()

    # Popolo le tabelle con i dati
    if User.query.first() is None:
        
        json_files = [
            
            ('lotti.json', Lotto) 
            ('prenotazioni.json', Prenotazione) 
            ('prodotti.json', Prodotto) 
            ('produttori.json', Produttore) 
            ('users.json', User)
        ]

        for filename, model in json_files:
            file_path = os.path.join(BASE_DIR, 'database', 'data_json',filename )
            print(file_path)
            

            with open(file_path, 'r') as file:
                lista_record = json.load(file)
            # pprint(lista_record)
            
            for record_dict in lista_record:
                if 'data_consegna' in record_dict:
                    var_data_consegna = date.fromisoformat(record_dict['data_consegna'])
                    record_dict['data_consegna'] = var_data_consegna
                new_record = model(**record_dict)
                db.session.add(new_record)
            db.session.commit()
