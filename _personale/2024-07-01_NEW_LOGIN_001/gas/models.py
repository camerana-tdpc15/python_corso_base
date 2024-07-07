
import json
import os
from datetime import date
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from settings import BASE_DIR



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
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), nullable=False)
    nome_prodotto = db.Column(db.String(50), nullable=False)

     # RELATIONSHIPS
    rel_lotti = db.relationship('Lotto', back_populates='rel_prodotto')
    
class Lotto(db.Model):
    __tablename__ = 'lotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, default=False)

    # RELATIONSHIPS
    rel_prodotto = db.relationship('Prodotto', back_populates='rel_lotti')
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_lotto')

    def get_date(self):
        res_data = self.data_consegna.strftime('%A %d/%m/%Y')
        return res_data

    def get_prezzo_str(self):
        return f'{self.prezzo_unitario} €/{self.qta_unita_misura}'

    def get_qta_disponibile(self):
        qta_prenotata = 0
        for prenot in self.rel_prenotazioni:
            qta_prenotata += prenot.qta
        
        return self.qta_lotto - qta_prenotata

class Prenotazione(db.Model):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)

     # RELATIONSHIPS
    rel_lotto = db.relationship('Lotto', back_populates='rel_prenotazioni')

def init_db():
    # crea le tabelle se non esestono gia'
    db.create_all()

    

    # popolo le tabelle se non esiste un record in User
    if User.query.first() is None:

        
        json_files = [

        ('lotti.json', Lotto),
        ('prenotazioni.json', Prenotazione),
        ('prodotti.json', Prodotto  ),
        ('produttori.json', Produttore ),
        ('users.json', User) 
        
        ]

        for filename, model in json_files:
            file_path = os.path.join(BASE_DIR, 'database', 'data_json', filename)
            print(file_path)
            
            with open(file_path, 'r') as file:
                
                lista_record = json.load(file)
            
            for record_dict in lista_record:

                if 'data_consegna' in record_dict:
                    var_data_consegna = date.fromisoformat(record_dict['data_consegna'])
                    record_dict['data_consegna'] = var_data_consegna
                
                new_record = model(**record_dict)

                db.session.add(new_record)
        db.session.commit()

           



           

        

   