import os
import json
from datetime import datetime
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from settings import BASE_DIR

db = SQLAlchemy()

class Utente(db.Model, SerializerMixin):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    # RELATIONSHIPS
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_utente')

    serialize_rules = ('-rel_prenotazioni.rel_utente', '-password')

class Replica(db.Model, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventi.id'), nullable=False)
    data_ora = db.Column(db.DateTime, nullable=False)
    annullato = db.Column(db.Boolean, default=False)
    # RELATIONSHIPS
    rel_evento = db.relationship('Evento', back_populates='rel_repliche')
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_replica')

    serialize_rules = ('-rel_evento.rel_repliche',
                       '-rel_prenotazioni.rel_replica')
    
    

class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)
    replica_id = db.Column(db.Integer, db.ForeignKey('repliche.id'), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)
    # RELATIONSHIPS
    rel_replica = db.relationship('Replica', back_populates='rel_prenotazioni')
    # non c'era nel app fatta in classe gas09
    rel_utente = db.relationship('Utente', back_populates='rel_prenotazioni')

    serialize_rules = ('-rel_replica.rel_prenotazioni', '-rel_utente.rel_prenotazioni')

    # Definisco un unique constraint per la coppia lotto_id e user_id
    # in modo che non sia possibile creare una prenotazione con i medesimi
    # user_id e lotto_id
    __table_args__ = (
        db.UniqueConstraint('replica_id', 'utente_id', name='replica_utente_unique'),
    )

  
    

class Locale(db.Model, SerializerMixin):
    __tablename__ = 'locali'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_locale = db.Column(db.String(50), nullable=False)
    luogo = db.Column(db.String(100), nullable=False)
    posti = db.Column(db.Integer, nullable=False)
    # RELATIONSHIPS
    rel_eventi = db.relationship('Evento', back_populates='rel_locale')

    serialize_rules = ('-rel_eventi.rel_locale',)

class Evento(db.Model, SerializerMixin):
    __tablename__ = 'eventi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locale_id = db.Column(db.Integer, db.ForeignKey('locali.id'), nullable=False)
    nome_evento = db.Column(db.String(50), nullable=False)
     # RELATIONSHIPS
    rel_repliche = db.relationship('Replica', back_populates='rel_evento')
    rel_locale = db.relationship('Locale', back_populates='rel_eventi')

    # Se dobbiamo escludere delle relazioni ricorsive dobbiamo
    # elencarle in "serialize_rules" con un '-'
    serialize_rules = ('-rel_repliche.rel_evento', '-rel_locale.rel_eventi')

    # Altrimenti, l'approccio inverso è quello di elencare solo i campi che
    # devono essere estratti. Ricordiamoci che non dobbiamo includere le relazioni
    # che provocano la ricorsione!
    # serialize_only = ('nome_prodotto', 'rel_produttore')
   
def init_db():
    # Crea le tabelle solo se non esistono già
    db.create_all()

    # Popolo le tabelle con i dati se non esiste un record in User
    if Utente.query.first() is None:
        # Creo una lista con i nomi dei file json e i modelli corrispondenti
        # in modo da sapere in quale tabella devono essere inseriti i dati di
        # ciascun file json
        json_files = [
            ('eventi.json', Evento),
            ('locali.json', Locale),
            ('prenotazioni.json', Prenotazione),
            ('repliche.json', Replica),
            ('utenti.json', Utente),
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
                if 'data_ora' in record_dict:
                    # Converto il valore della 'data_consegna' in un oggetto date

                    # Converto il valore della 'data_consegna' in un oggetto date
                    date_str = record_dict['data_ora']
                    
                    # Definisci il formato originale della data
                    original_format = "%d-%m-%Y-%H:%M:%S"

                    # Converte la stringa della data in un oggetto datetime
                    date_obj = datetime.strptime(date_str, original_format)

                    # Converte l'oggetto datetime nel formato ISO 8601
                    record_dict['data_ora'] = date_obj


                # Creo un nuovo record del modello corrispondente
                new_record = model(**record_dict)
                # Aggiungo il record alla sessione
                db.session.add(new_record)
        
        # Eseguo il commit della sessione per scrivere i dati nel database
        db.session.commit()
