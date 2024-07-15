import os
import json
from datetime import date, datetime
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from settings import BASE_DIR

db = SQLAlchemy()

class utente(db.Model, SerializerMixin):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    serialize_rules = ('-password',)
    #relazioni
    rel_prenotazioni= db.relationship('prenotazione',  back_populates='rel_utenti')

    serialize_rules =('-rel_prenotazioni.rel_utenti')


class prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)
    replica_id = db.Column(db.Integer, db.ForeignKey('repliche.id'), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)

    #relazioni
    rel_utenti= db.relationship('utente',  back_populates='rel_prenotazioni')
    rel_repliche= db.relationship('replica',  back_populates='rel_prenotazioni')

    serialize_rules =('-rel_utenti.rel_prenotazioni', '-rel_repliche.rel_prenotazioni')
    
class replica(db.Model, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventi.id'), nullable=False)
    data_ora = db.Column(db.DateTime, nullable=False)
    annullato = db.Column(db.Boolean, nullable=False)

    #relazioni
    rel_eventi= db.relationship('evento',  back_populates='rel_repliche')
    rel_prenotazioni= db.relationship('prenotazione',  back_populates='rel_repliche')

    serialize_rules =('-rel_eventi.rel_repliche', '-rel_prenotazioni.rel_repliche')


class evento(db.Model, SerializerMixin):
    __tablename__= 'eventi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locale_id = db.Column(db.Integer, db.ForeignKey('locali.id'), nullable=False)
    nome_evento = db.Column(db.String(50), nullable=False)

    #relazioni
    rel_locali= db.relationship('locale',  back_populates='rel_eventi')
    rel_repliche= db.relationship('replica',  back_populates='rel_eventi')

    serialize_rules =('-rel_locali.rel_eventi', '-rel_repliche.rel_eventi')


class locale(db.Model, SerializerMixin):
    __tablename__ = 'locali'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_locale = db.Column(db.String(50), nullable=False)
    luogo = db.Column(db.String(100), nullable=False)
    posti = db.Column(db.Integer, nullable=False) 

    #relazioni
    rel_eventi= db.relationship('evento',  back_populates='rel_locali')

    serialize_rules =('-rel_eventi.rel_locali')  


def init_db():
    # Crea le tabelle solo se non esistono già
    db.create_all() 

      # Popolo le tabelle con i dati se non esiste un record in User
    if utente.query.first() is None:
        # Creo una lista con i nomi dei file json e i modelli corrispondenti
        # in modo da sapere in quale tabella devono essere inseriti i dati di
        # ciascun file json
        json_files = [
            ('eventi.json', evento),
            ('locali.json', locale),
            ('prenotazioni.json', prenotazione),
            ('repliche.json', replica),
            ('utenti.json', utente),
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
                    # Converto il valore della 'data_ora' in un oggetto date
                    var_data_ora = datetime.strptime( record_dict['data_ora'], '%d-%m-%Y-%H:%M:%S')
                    record_dict['data_ora'] = var_data_ora

                # Creo un nuovo record del modello corrispondente
                new_record = model(**record_dict)
                # Aggiungo il record alla sessione
                db.session.add(new_record)
        
        # Eseguo il commit della sessione per scrivere i dati nel database
        db.session.commit()
