import os
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from settings import BASE_DIR

db = SQLAlchemy()

# Funzione per convertire il formato del timestamp
def convert_timestamp(timestamp):
    return datetime.strptime(timestamp, '%d-%m-%Y-%H:%M:%S').isoformat()

# Modello per la tabella 'utenti'
class Utente(db.Model, SerializerMixin):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    ruolo = db.Column(db.String(20), nullable=False)

    # Relazione con la tabella 'prenotazioni'
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_utente')

    serialize_rules = ('-password', '-rel_prenotazioni.rel_utente')

    @validates('password')
    def convert_to_hash(self, key, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Modello per la tabella 'prenotazioni'
class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)
    replica_id = db.Column(db.Integer, db.ForeignKey('repliche.id'), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)

    # Relazioni con le tabelle 'utenti' e 'repliche'
    rel_utente = db.relationship('Utente', back_populates='rel_prenotazioni')
    rel_replica = db.relationship('Replica', back_populates='rel_prenotazioni')

    serialize_rules = ('-rel_utente.rel_prenotazioni', '-rel_replica.rel_prenotazioni')

# Modello per la tabella 'repliche'
class Replica(db.Model, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventi.id'), nullable=False)
    data_ora = db.Column(db.DateTime, nullable=False)
    annullato = db.Column(db.Boolean, default=False)

    # Relazione con la tabella 'prenotazioni'
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_replica')
    # Relazione con la tabella 'eventi'
    rel_evento = db.relationship('Evento', back_populates='rel_repliche')

    serialize_rules = ('-rel_prenotazioni.rel_replica', '-rel_evento.rel_repliche')

    # Funzione per ottenere la data di consegna come stringa formattata
    def get_date(self):
        res_data = self.data_ora.strftime('%H:%M %A %d/%m/%Y')
        return res_data  # es. "Giovedì 27/06/2024"

    # Funzione per ottenere i posti disponibili
    def posti_disponibili(self):
        posti_prenotati = sum([prenotazione.quantita for prenotazione in self.rel_prenotazioni])
        return self.rel_evento.rel_locale.posti - posti_prenotati
    
    # Restituisce un dizionario con i dettagli della replica, inclusi i posti disponibili
    def to_dict_with_details(self):
        replica_dict = self.to_dict()
        replica_dict['posti_disponibili'] = self.posti_disponibili()
        replica_dict['data_ora'] = self.get_date()
        replica_dict['annullato'] = self.annullato
        return replica_dict  

# Modello per la tabella 'eventi'
class Evento(db.Model, SerializerMixin):
    __tablename__ = 'eventi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locale_id = db.Column(db.Integer, db.ForeignKey('locali.id'), nullable=False)
    nome_evento = db.Column(db.String(50), nullable=False)
    immagine = db.Column(db.String(50))  # Nuovo campo per il nome dell'immagine

    # Relazione con la tabella 'repliche'
    rel_repliche = db.relationship('Replica', back_populates='rel_evento')
    # Relazione con la tabella 'locali'
    rel_locale = db.relationship('Locale', back_populates='rel_eventi')

    serialize_rules = ('-rel_repliche.rel_evento', '-rel_locale.rel_eventi')

    # Restituisce un dizionario con i dettagli dell'evento, inclusi locale e repliche
    def to_dict_with_details(self):       
        evento_dict = self.to_dict()
        evento_dict['luogo'] = self.rel_locale.luogo
        evento_dict['nome_locale'] = self.rel_locale.nome_locale
        evento_dict['repliche'] = [replica.to_dict_with_details() for replica in self.rel_repliche]
        return evento_dict

# Modello per la tabella 'locali'
class Locale(db.Model, SerializerMixin):
    __tablename__ = 'locali'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_locale = db.Column(db.String(50), nullable=False)
    luogo = db.Column(db.String(100), nullable=False)
    posti = db.Column(db.Integer, nullable=False)

    # Relazione con la tabella 'eventi'
    rel_eventi = db.relationship('Evento', back_populates='rel_locale')

    serialize_rules = ('-rel_eventi.rel_locale',)

# Funzione per inizializzare il database
def init_db():
    # Crea le tabelle solo se non esistono già
    db.create_all()

    # Popolo le tabelle con i dati se non esiste un record in Utente
    if Utente.query.first() is None:
        # Creo una lista con i nomi dei file json e i modelli corrispondenti
        # in modo da sapere in quale tabella devono essere inseriti i dati di
        # ciascun file json
        json_files = [
            ('utenti.json', Utente),
            ('prenotazioni.json', Prenotazione),
            ('repliche.json', Replica),
            ('eventi.json', Evento),
            ('locali.json', Locale),
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
                # Se la chiave 'data_ora' è presente nel dizionario
                if 'data_ora' in record_dict:
                    # Converto il valore della 'data_ora' in un oggetto datetime
                    record_dict['data_ora'] = datetime.fromisoformat(convert_timestamp(record_dict['data_ora']))

                # Creo un nuovo record del modello corrispondente
                new_record = model(**record_dict)
                # Aggiungo il record alla sessione
                db.session.add(new_record)
        
        # Eseguo il commit della sessione per scrivere i dati nel database
        db.session.commit()

if __name__ == '__main__':
    # Inizializza il database
    init_db()