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

    serialize_rules = ('-password',)

class Produttore(db.Model, SerializerMixin):
    __tablename__ = 'produttori'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produttore = db.Column(db.String(), unique=True, nullable=False)
    descrizione = db.Column(db.Text(), nullable=False)
    indirizzo = db.Column(db.Text(), nullable=False)
    telefono = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    # RELATIONSHIPS
    rel_prodotti = db.relationship('Prodotto', back_populates='rel_produttore')

    serialize_rules = ('-rel_prodotti.rel_produttore',)

class Prodotto(db.Model, SerializerMixin):
    __tablename__ = 'prodotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), nullable=False)
    nome_prodotto = db.Column(db.String(50), nullable=False)
    # RELATIONSHIPS
    rel_lotti = db.relationship('Lotto', back_populates='rel_prodotto')
    rel_produttore = db.relationship('Produttore', back_populates='rel_prodotti')

    # Se dobbiamo escludere delle relazioni ricorsive dobbiamo
    # elencarle in "serialize_rules" con un '-'
    serialize_rules = ('-rel_lotti.rel_prodotto', '-rel_produttore.rel_prodotti')

    # Altrimenti, l'approccio inverso è quello di elencare solo i campi che
    # devono essere estratti. Ricordiamoci che non dobbiamo includere le relazioni
    # che provocano la ricorsione!
    # serialize_only = ('nome_prodotto', 'rel_produttore')


class Lotto(db.Model, SerializerMixin):
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

    serialize_rules = ('-rel_prodotto.rel_lotti', '-rel_prenotazioni.rel_lotto', 'get_date', 'get_prezzo_str', 'get_qta_disponibile')

    # serialize_only = (
    #     'data_consegna',
    #     'qta_unita_misura',
    #     'qta_lotto',
    #     'prezzo_unitario',
    #     'sospeso',
    #     'rel_prodotto',
    #     'get_date',
    #     'get_prezzo_str',
    #     'get_qta_disponibile',
    # )

    def get_date(self):
        res_data = self.data_consegna.strftime('%A %d/%m/%Y')
        return res_data  # es. "Giovedì 27/06/2024"

    def get_prezzo_str(self):
        return f'{self.prezzo_unitario} €/{self.qta_unita_misura}'  # es. "8.50 €/L"

    def get_qta_disponibile(self):
        qta_prenotata = 0
        for prenot in self.rel_prenotazioni:
            qta_prenotata += prenot.qta
        
        return self.qta_lotto - qta_prenotata

class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)
    # RELATIONSHIPS
    rel_lotto = db.relationship('Lotto', back_populates='rel_prenotazioni')

    serialize_rules = ('-rel_lotto.rel_prenotazioni',)

    # Definisco un unique constraint per la coppia lotto_id e user_id
    # in modo che non sia possibile creare una prenotazione con i medesimi
    # user_id e lotto_id
    __table_args__ = (
        db.UniqueConstraint('lotto_id', 'user_id', name='lotto_user_unique'),
    )

def init_db():
    # Crea le tabelle solo se non esistono già
    db.create_all()

    # Popolo le tabelle con i dati se non esiste un record in User
    if User.query.first() is None:
        # Creo una lista con i nomi dei file json e i modelli corrispondenti
        # in modo da sapere in quale tabella devono essere inseriti i dati di
        # ciascun file json
        json_files = [
            ('lotti.json', Lotto),
            ('prenotazioni.json', Prenotazione),
            ('prodotti.json', Prodotto),
            ('produttori.json', Produttore),
            ('users.json', User),
        ]

        # Itero a coppie il nome del file json e il modello corrispondente
        for filename, model in json_files:
            # Compone il path al file json
            file_path = os.path.join(BASE_DIR, 'database', 'data_json', filename)

            # Apro il file json in lettura
            with open(file_path, 'r') as file:
                # Leggo il contenuto del file json e ottengo una lista di dizionari
                lista_record = json.load(file)

            # Itero la lista di dizionari
            for record_dict in lista_record:
                # Se la chiave 'data_consegna' è presente nel dizionario
                if 'data_consegna' in record_dict:
                    # Converto il valore della 'data_consegna' in un oggetto date
                    var_data_consegna = date.fromisoformat(record_dict['data_consegna'])
                    record_dict['data_consegna'] = var_data_consegna

                # Creo un nuovo record del modello corrispondente
                new_record = model(**record_dict)
                # Aggiungo il record alla sessione
                db.session.add(new_record)
        
        # Eseguo il commit della sessione per scrivere i dati nel database
        db.session.commit()
