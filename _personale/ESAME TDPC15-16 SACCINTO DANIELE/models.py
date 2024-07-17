import os
import json
from datetime import date, datetime
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from settings import BASE_DIR

# Inizializzazione dell'oggetto SQLAlchemy
db = SQLAlchemy()

# Definizione della classe Utente che rappresenta la tabella 'utenti'
class Utente(db.Model, SerializerMixin):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    # Relazione con la tabella 'prenotazioni'
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_utenti')

# Definizione della classe Prenotazione che rappresenta la tabella 'prenotazioni'
class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)
    replica_id = db.Column(db.Integer, db.ForeignKey('repliche.id'), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)

    # Relazione con la tabella 'utenti'
    rel_utenti = db.relationship('Utente', back_populates='rel_prenotazioni')
    # Relazione con la tabella 'repliche'
    rel_repliche = db.relationship('Replica', back_populates='rel_prenotazioni')

# Definizione della classe Replica che rappresenta la tabella 'repliche'
class Replica(db.Model, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventi.id'), nullable=False)
    data_ora = db.Column(db.DateTime, nullable=False)
    annullato = db.Column(db.Boolean, nullable=False)

    # Relazione con la tabella 'eventi'
    rel_eventi = db.relationship('Evento', back_populates='rel_repliche')
    # Relazione con la tabella 'prenotazioni'
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_repliche')

    # Metodo per ottenere la data formattata
    def get_date(self):
        return self.data_ora.strftime('%A %d/%m/%Y')

    # Metodo per ottenere la quantità disponibile
    def get_qta_disponibile(self):
        qta_prenotata = sum(prenot.quantita for prenot in self.rel_prenotazioni)
        return self.rel_eventi.rel_locali.posti - qta_prenotata

# Definizione della classe Evento che rappresenta la tabella 'eventi'
class Evento(db.Model, SerializerMixin):
    __tablename__ = 'eventi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locale_id = db.Column(db.Integer, db.ForeignKey('locali.id'), nullable=False)
    nome_evento = db.Column(db.String(50), nullable=False)

    # Relazione con la tabella 'locali'
    rel_locali = db.relationship('Locale', back_populates='rel_eventi')
    # Relazione con la tabella 'repliche'
    rel_repliche = db.relationship('Replica', back_populates='rel_eventi')

# Definizione della classe Locale che rappresenta la tabella 'locali'
class Locale(db.Model, SerializerMixin):
    __tablename__ = 'locali'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_locale = db.Column(db.String(50), nullable=False)
    luogo = db.Column(db.String(100), nullable=False)
    posti = db.Column(db.Integer, nullable=False)

    # Relazione con la tabella 'eventi'
    rel_eventi = db.relationship('Evento', back_populates='rel_locali')

# Funzione per inizializzare il database
def init_db():
    db.create_all()  # Crea tutte le tabelle definite

    # Se non ci sono utenti, importa i dati dai file JSON
    if Utente.query.first() is None:
        json_files = [
            ('eventi.json', Evento),
            ('locali.json', Locale),
            ('prenotazioni.json', Prenotazione),
            ('repliche.json', Replica),
            ('utenti.json', Utente),
        ]

        # Percorre i file JSON e inserisce i dati nel database
        for filename, model in json_files:
            file_path = os.path.join(BASE_DIR, 'database', 'data_json', filename)

            with open(file_path, 'r') as file:
                lista_record = json.load(file)

            # Converte i record e li aggiunge al database
            for record_dict in lista_record:
                if 'data_ora' in record_dict:
                    record_dict['data_ora'] = datetime.strptime(record_dict['data_ora'], '%d-%m-%Y-%H:%M:%S')

                new_record = model(**record_dict)
                db.session.add(new_record)

        db.session.commit()  # Commette tutte le modifiche