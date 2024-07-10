import os
import json
from datetime import date
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from settings import BASE_DIR

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    serializer_rules = ('-password',)

class Produttore(db.Model, SerializerMixin):
    __tablename__ = 'produttori'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produttore = db.Column(db.String(), unique=True, nullable=False)
    descrizione = db.Column(db.Text(), nullable=False)
    indirizzo = db.Column(db.Text(), nullable=False)
    telefono = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)

    rel_prodotti = db.relationship('Prodotto', back_populates = 'rel_produttore')

    les = ('-rel_prodotti.rel_produttore',)


class Prodotto(db.Model, SerializerMixin):
    __tablename__ = 'prodotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), nullable=False)
    nome_prodotto = db.Column(db.String(50), nullable=False)

#RELATIONSHIPS
    rel_lotti = db.relationship('Lotto', back_populates = 'rel_prodotti')
    rel_produttore = db.relationship('Produttore', back_populates=' rel_prodotti ')

    serialize_rules = ('-rel_lotti.rel_prodotto', '-rel_produttore.rel_prodotti')

class Lotto(db.Model, SerializerMixin):
    __tablename__ = 'lotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, default=False)

#RELATIONSHIPS
    rel_prodotto = db.relationship('Prodotto', back_populates = 'rel_lotti')
    rel_prenotazioniì= db.relationship('Prenotazione', back_populates = 'rel_lotto')

    serialize_rules = ('-rel_prodotto.rel_lotti', 'get_date', 'get_prezzo_str', 'get_qta_disponibile')


    def get_date(self):
        res_data = self.data_consegna.strftime('%A %d/%m/%Y')
        return res_data
    
    def get_prezzo_str(self):
        return f'{self.prezzo_unitario} €/{self.qta_unita_misura}'
    
    def get_qta_disponibile(self):
        qta_prenotate = 0
        for prenot in self.rel_prenotazioniì:
            qta_prenotate += prenot.qta

        return self.qta_lotto - qta_prenotate


class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)
#RELATIONSHIPS
    
    rel_lotto = db.relationship('Lotto',back_populates = 'rel_prenotazioni')

    serialize_rules = ('-rel_lotto.rel_prenotazioni',)
    # Definisco un unique constraint per la coppia lotto_id e user_idin modo che 
    #   non sia possibile creare una prenotazione con i medesimi user_id e lotto_id
    
    __table_args__ = (
        db.UniqueConstraint('lotto_id', 'user_id', name = 'lotto_user_unique'),
    )

def init_db():
    # Crea le tabelle se non esistono già
    db.create_all()

    # Popolo le tabelle con i dati
    if User.query.first() is None:
        
        json_files = [
            
            ('lotti.json', Lotto), 
            ('prenotazioni.json', Prenotazione),
            ('prodotti.json', Prodotto), 
            ('produttori.json', Produttore), 
            ('users.json', User),
        ]

        for filename, model in json_files:
            file_path = os.path.join(BASE_DIR, 'database', 'data_json',filename )
            
            

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
