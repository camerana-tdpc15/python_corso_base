
import locale
import os
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from settings import BASE_DIR_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

db = SQLAlchemy()

class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.mapped_column(db.Integer(), primary_key=True, autoincrement=True)
    utente_id = db.mapped_column(db.Integer(), db.ForeignKey('utenti.id'))
    replica_id = db.mapped_column(db.Integer(), db.ForeignKey('repliche.id'))
    quantita = db.mapped_column(db.Integer(), nullable=False)
    # -- RELATIONSHIPS --
    rel_utente = db.relationship('Utente', back_populates='rel_prenotazioni')
    rel_replica = db.relationship('Replica', back_populates='rel_prenotazioni')

    serialize_rules = ('-rel_utente.rel_prenotazioni', '-rel_replica.rel_prenotazioni')



class Utente(db.Model, SerializerMixin):
    __tablename__ = 'utenti'
    id = db.mapped_column(db.Integer(), primary_key=True)
    cognome = db.mapped_column(db.String(100), nullable=False)
    nome = db.mapped_column(db.String(100), nullable=False)
    telefono = db.mapped_column(db.String(20), nullable=False)
    email = db.mapped_column(db.String(50), nullable=False)
    password = db.mapped_column(db.String(30), nullable=False)    
    # -- RELATIONSHIPS --
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_utente')

    serialize_rules = ('-rel_prenotazioni.rel_utente', '-password')



class Replica(db.Model, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.mapped_column(db.Integer(), primary_key=True)
    evento_id = db.mapped_column(db.Integer(), db.ForeignKey('eventi.id'), nullable=False)
    data_ora = db.mapped_column(db.DateTime(), nullable=False)
    annullato = db.mapped_column(db.Boolean(), default=False)        
    # -- RELATIONSHIPS --
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_replica')
    rel_evento = db.relationship('Evento', back_populates='rel_repliche')

    serialize_rules = ('-rel_prenotazioni.rel_replica', '-rel_evento.rel_repliche')




class Evento(db.Model, SerializerMixin):
    __tablename__ = 'eventi'
    id = db.mapped_column(db.Integer(), primary_key=True)
    locale_id = db.mapped_column(db.Integer(), db.ForeignKey('locali.id'), nullable=False)
    nome_evento = db.mapped_column(db.String(100), nullable=False)
    immagine = db.mapped_column(db.String(100), nullable=False)
    # -- RELATIONSHIPS --
    rel_repliche = db.relationship('Replica', back_populates='rel_evento')
    rel_locale = db.relationship('Locale', back_populates='rel_eventi')

    serialize_rules = ('-rel_repliche.rel_evento', '-rel_locale.rel_eventi')


    

class Locale(db.Model, SerializerMixin):
    __tablename__ = 'locali'
    id = db.mapped_column(db.Integer(), primary_key=True)
    nome_locale = db.mapped_column(db.String(100), nullable=False)
    luogo = db.mapped_column(db.String(100), nullable=False)
    posti = db.mapped_column(db.Integer(), nullable=False)
    # -- RELATIONSHIPS --
    rel_eventi = db.relationship('Evento', back_populates='rel_locale')

    serialize_rules = ('-rel_eventi.rel_locale',)
    
    
# Funzione per convertire una stringa datetime in un oggetto datetime
def converti_datetime(dt_string):
    day, month, year, time = dt_string.split('-')
    hour, minute, second = time.split(':')
    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))



def init_db():
    #db.init_app(app)
    #with app.app_context():
        # Crea le tabelle solo se non esistono già
    db.create_all()

    # Popolo le tabelle con i dati se non esiste un record in Utente
    if Utente.query.first() is None:
        # Creo una lista con i nomi dei file json e i modelli corrispondenti
        # in modo da sapere in quale tabella devono essere inseriti i dati di
        # ciascun file json
        json_files = [
            ('eventi.json', Evento),
            ('prenotazioni.json', Prenotazione),
            ('locali.json', Locale),
            ('repliche.json', Replica),
            ('utenti.json', Utente),
        ]

        # Itero a coppie il nome del file json e il modello corrispondente
        for filename, model in json_files:
            # Compone il path al file json
            file_path = os.path.join(BASE_DIR_PATH, 'database', filename)

            # Apro il file json in lettura
            with open(file_path, 'r') as file:
                # Leggo il contenuto del file json e ottengo una lista di dizionari
                lista_record = json.load(file)

            # Itero la lista di dizionari
            for record_dict in lista_record:
                # Se la chiave 'data_consegna' è presente nel dizionario
                if 'data_ora' in record_dict:
                #     # Converto il valore della 'data_consegna' in un oggetto datetime
                    var_data_ora = datetime.strptime(record_dict['data_ora'],'%d-%m-%Y-%H:%M:%S')
                    record_dict['data_ora'] = var_data_ora

                # Creo un nuovo record del modello corrispondente
                new_record = model(**record_dict)
                # Aggiungo il record alla sessione
                db.session.add(new_record)
        
        # Eseguo il commit della sessione per scrivere i dati nel database
        db.session.commit()

    
    