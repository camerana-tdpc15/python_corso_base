import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from settings import BASE_DIR

# Inizializza SQLAlchemy
db = SQLAlchemy()

# Definisci il modello Locale
class Locale(db.Model, SerializerMixin):
    __tablename__ = 'locali'
    id = db.Column(db.Integer, primary_key=True)  # Chiave primaria
    nome_locale = db.Column(db.String(50), nullable=False)  # Nome del locale
    luogo = db.Column(db.String(100), nullable=False)  # Luogo
    posti = db.Column(db.Integer, nullable=False)  # Numero di posti

    # Relazione con Evento
    rel_eventi = db.relationship('Evento', back_populates='rel_locale', lazy=True)

    serialize_rules = ('-rel_eventi.rel_locale',)

# Definisci il modello Evento
class Evento(db.Model, SerializerMixin):
    __tablename__ = 'eventi'
    id = db.Column(db.Integer, primary_key=True)  # Chiave primaria
    locale_id = db.Column(db.Integer, db.ForeignKey('locali.id'), nullable=False)  # Chiave esterna per Locale
    nome_evento = db.Column(db.String(50), nullable=False)  # Nome dell'evento

    # Relazioni
    rel_locale = db.relationship('Locale', back_populates='rel_eventi', lazy=True)
    rel_repliche = db.relationship('Replica', back_populates='rel_evento', lazy=True)

    serialize_rules = ('-rel_locale.rel_eventi', '-rel_repliche.rel_evento')

# Definisci il modello Replica
class Replica(db.Model, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.Column(db.Integer, primary_key=True)  # Chiave primaria
    evento_id = db.Column(db.Integer, db.ForeignKey('eventi.id'), nullable=False)  # Chiave esterna per Evento
    data_ora = db.Column(db.DateTime, nullable=False)  # Data e ora della replica
    annullato = db.Column(db.Boolean, default=False)  # Stato di annullamento

    # Relazioni
    rel_evento = db.relationship('Evento', back_populates='rel_repliche', lazy=True)
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_replica', lazy=True)

    serialize_rules = ('-rel_evento.rel_repliche', '-rel_prenotazioni.rel_replica')

# Definisci il modello Utente
class Utente(db.Model, SerializerMixin):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)  # Chiave primaria
    cognome = db.Column(db.String(50), nullable=False)  # Cognome
    nome = db.Column(db.String(50), nullable=False)  # Nome
    telefono = db.Column(db.String(20))  # Telefono
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email
    password = db.Column(db.String(30), nullable=False) # Password

    # Relazioni
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_utente', lazy=True)

    serialize_rules = ('-rel_prenotazioni.rel_utente',)

# Definisci il modello Prenotazione
class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True)  # Chiave primaria
    utente_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)  # Chiave esterna per Utente
    replica_id = db.Column(db.Integer, db.ForeignKey('repliche.id'), nullable=False)  # Chiave esterna per Replica
    quantita = db.Column(db.Integer, nullable=False)  # Quantità di prenotazioni

    # Relazioni
    rel_utente = db.relationship('Utente', back_populates='rel_prenotazioni', lazy=True)
    rel_replica = db.relationship('Replica', back_populates='rel_prenotazioni', lazy=True)

    serialize_rules = ('-rel_utente.rel_prenotazioni', '-rel_replica.rel_prenotazioni')

# Funzione per convertire una stringa datetime in un oggetto datetime
def converti_datetime(dt_string):
    day, month, year, time = dt_string.split('-')
    hour, minute, second = time.split(':')
    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

# Funzione per inizializzare il database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        # Crea le tabelle solo se non esistono già
        db.create_all()

        # Popola le tabelle con i dati se non esiste un record in Utente
        if Utente.query.first() is None:
            # Crea una lista con i nomi dei file json e i modelli corrispondenti
            json_files = [
                ('utenti.json', Utente),
                ('prenotazioni.json', Prenotazione),
                ('repliche.json', Replica),
                ('eventi.json', Evento),
                ('locali.json', Locale),
            ]

            for filename, model in json_files:
                file_path = os.path.join(BASE_DIR, 'database', 'data_json', filename)
                with open(file_path, 'r') as file:
                    lista_record = json.load(file)

                for record_dict in lista_record:
                    if 'data_ora' in record_dict:
                        record_dict['data_ora'] = converti_datetime(record_dict['data_ora'])
                    new_record = model(**record_dict)
                    db.session.add(new_record)
            
            db.session.commit()

if __name__ == '__main__':
    # Inizializza il database
    init_db()