
import csv
import os
import sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from settings import LOTTO_TABLE_CSV, LOTTO_TABLE_NAME, PRENOTAZIONE_TABLE_CSV, PRENOTAZIONE_TABLE_NAME, PRODOTTO_TABLE_CSV, PRODOTTO_TABLE_NAME, PRODUTTORE_TABLE_CSV, PRODUTTORE_TABLE_NAME, USER_TABLE_CSV, USER_TABLE_NAME

db = SQLAlchemy()   # creo istanza SQLAlchemy

# creo la struttura delle tabelle
class User(db.Model):        # nome della classe al singolare e iniziale maiuscola, nome della tabella plurale
    __tablename__ = USER_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    prenotazioni = db.relationship('Prenotazione', back_populates='utente')

class Produttore(db.Model):
    __tablename__ = PRODUTTORE_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    nome_produttore = db.Column(db.String(150), nullable=False)
    descrizione = db.Column(db.String(250))
    indirizzo = db.Column(db.String(250))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(150))
    prodotti = db.relationship('Prodotto', back_populates='produttore')

class Prodotto(db.Model):
    __tablename__ = PRODOTTO_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttore.id'), nullable=False)
    nome_prodotto = db.Column(db.String(150), nullable=False)
    produttore = db.relationship('Produttore', back_populates='prodotti')
    lotti = db.relationship('Lotto', back_populates='prodotto')


class Lotto(db.Model):
    __tablename__ = LOTTO_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotto.id'), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, default=False)
    prodotto = db.relationship('Prodotto', back_populates='lotti')
    prenotazioni = db.relationship('Prenotazione', back_populates='lotto')


class Prenotazione(db.Model):
    __tablename__ = PRENOTAZIONE_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotto.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)
    utente = db.relationship('User', back_populates='prenotazioni')
    lotto = db.relationship('Lotto', back_populates='prenotazioni')


# def init_db(app):
#     # Crea le tabelle nel database, se queste non esistono già
#     db.create_all()

#     # Se la tabella NON è già popolata
#     if not User.query.first():
#         # Se il file CSV esiste
#         if os.path.exists(USER_TABLE_CSV):
#             # Apre il file CSV in lettura
#             with open(USER_TABLE_CSV, 'r') as csv_file:
#                 # Legge il file CSV come dizionario
#                 csv_reader = csv.DictReader(csv_file)
#                 # Per ogni riga del file CSV
#                 for row in csv_reader:
#                     # Crea un oggetto User con i valori della riga corrente
#                     new_record = User(
#                         cognome=row['cognome'],
#                         nome=row['nome'],
#                         telefono=row['telefono'],
#                         email=row['email'],
#                         password=row['password']
#                     )
#                     # Aggiunge l'oggetto User al database
#                     db.session.add(new_record)
#                 # Conferma le modifiche al database
#                 db.session.commit()
#                 app.logger.info(f'Tabella "{USER_TABLE_NAME}" popolata correttamente.')
#         else:
#             app.logger.error(
#                 f'Il file "{USER_TABLE_CSV}" non esiste. '
#                 'Verifica il percorso e riprova.'
#             )
#             sys.exit(1)
#     else:
#         app.logger.info(f'Tabella "{USER_TABLE_NAME}" già popolata.')

#     if not Produttore.query.first():
#         if os.path.exists(PRODUTTORE_TABLE_CSV):
#             with open(PRODUTTORE_TABLE_CSV, 'r') as csv_file:
#                 csv_reader = csv.DictReader(csv_file)
#                 for row in csv_reader:
#                     new_record = Produttore(
#                         nome_produttore=row['nome_produttore'],
#                         descrizione=row['descrizione'],
#                         indirizzo=row['indirizzo'],
#                         telefono=row['telefono'],
#                         email=row['email']
#                     )
#                     db.session.add(new_record)
#                 db.session.commit()
#                 app.logger.info(f'Tabella "{PRODUTTORE_TABLE_NAME}" popolata correttamente.')
#         else:
#             app.logger.error(
#                 f'Il file "{PRODUTTORE_TABLE_CSV}" non esiste. '
#                 'Verifica il percorso e riprova.'
#             )
#             sys.exit(1)
#     else:
#         app.logger.info(f'Tabella "{PRODUTTORE_TABLE_NAME}" già popolata.')

#     if not Prodotto.query.first():
#         if os.path.exists(PRODOTTO_TABLE_CSV):
#             with open(PRODOTTO_TABLE_CSV, 'r') as csv_file:
#                 csv_reader = csv.DictReader(csv_file)
#                 for row in csv_reader:
#                     new_record = Prodotto(
#                         produttore_id=row['produttore_id'],
#                         nome_prodotto=row['nome_prodotto'],
#                     )
#                     db.session.add(new_record)
#                 db.session.commit()
#                 app.logger.info(f'Tabella "{PRODOTTO_TABLE_NAME}" popolata correttamente.')
#         else:
#             app.logger.error(
#                 f'Il file "{PRODOTTO_TABLE_CSV}" non esiste. '
#                 'Verifica il percorso e riprova.'
#             )
#             sys.exit(1)
#     else:
#         app.logger.info(f'Tabella "{PRODOTTO_TABLE_NAME}" già popolata.')

#     if not Lotto.query.first():
#         if os.path.exists(LOTTO_TABLE_CSV):
#             with open(LOTTO_TABLE_CSV, 'r') as csv_file:
#                 csv_reader = csv.DictReader(csv_file)
#                 for row in csv_reader:
#                     new_record = Lotto(
#                         prodotto_id=row['prodotto_id'],
#                         data_consegna=datetime.strptime(row['data_consegna'], '%Y-%m-%d'),
#                         qta_unita_misura=row['qta_unita_misura'],
#                         qta_lotto=row['qta_lotto'],
#                         prezzo_unitario=row['prezzo_unitario'],
#                         sospeso=row['sospeso'],
#                     )
#                     db.session.add(new_record)
#                 db.session.commit()
#                 app.logger.info(f'Tabella "{LOTTO_TABLE_NAME}" popolata correttamente.')
#         else:
#             app.logger.error(
#                 f'Il file "{LOTTO_TABLE_CSV}" non esiste. '
#                 'Verifica il percorso e riprova.'
#             )
#             sys.exit(1)
#     else:
#         app.logger.info(f'Tabella "{LOTTO_TABLE_NAME}" già popolata.')

#     if not Prenotazione.query.first():
#         if os.path.exists(PRENOTAZIONE_TABLE_CSV):
#             with open(PRENOTAZIONE_TABLE_CSV, 'r') as csv_file:
#                 csv_reader = csv.DictReader(csv_file)
#                 for row in csv_reader:
#                     new_record = Prenotazione(
#                         utente_id=row['utente_id'],
#                         lotto_id=row['lotto_id'],
#                         qta=row['qta'],
#                     )
#                     db.session.add(new_record)
#                 db.session.commit()
#                 app.logger.info(f'Tabella "{PRENOTAZIONE_TABLE_NAME}" popolata correttamente.')
#         else:
#             app.logger.error(
#                 f'Il file "{PRENOTAZIONE_TABLE_CSV}" non esiste. '
#                 'Verifica il percorso e riprova.'
#             )
#             sys.exit(1)
#     else:
#         app.logger.info(f'Tabella "{PRENOTAZIONE_TABLE_NAME}" già popolata.')

def init_db(app):
    #db.init_app(app)
    
    with app.app_context(): # attivo il contesto dell'app
        db.create_all()     # crea tutte le tabelle
        
        populate_table(User, USER_TABLE_CSV, app)
        populate_table(Produttore, PRODUTTORE_TABLE_CSV, app)
        populate_table(Prodotto, PRODOTTO_TABLE_CSV, app)
        populate_table(Lotto, LOTTO_TABLE_CSV, app, date_fields=['data_consegna'])
        populate_table(Prenotazione, PRENOTAZIONE_TABLE_CSV, app)

def populate_table(model, csv_file_path, app, date_fields=[]):
    if not model.query.first():
        if os.path.exists(csv_file_path):
            try:
                with open(csv_file_path, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        for field in date_fields:
                            row[field] = datetime.strptime(row[field], '%Y-%m-%d')
                        new_record = model(**row)
                        db.session.add(new_record)
                    db.session.commit()
                    app.logger.info(f'Tabella "{model.__tablename__}" popolata correttamente.')
            except Exception as e:
                app.logger.error(f'Errore durante la popolazione della tabella "{model.__tablename__}": {e}')
                sys.exit(1)
        else:
            app.logger.error(f'Il file "{csv_file_path}" non esiste. Verifica il percorso e riprova.')
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{model.__tablename__}" già popolata.')