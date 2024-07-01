import csv
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from settings import USERS_TABLE_NAME,LOTTI_TABLE_NAME, PRENOTAZIONI_TABLE_NAME, PRODOTTI_TABLE_NAME,PRODUTTORI_TABLE_NAME,USERS_TABLE_CSV,LOTTI_TABLE_CSV,PRENOTAZIONI_TABLE_CSV,PRODOTTI_TABLE_CSV,PRODUTTORI_TABLE_CSV

db = SQLAlchemy()  # Crea l'istanza di SQLAlchemy



class users(db.Model):
    __tablename__ = USERS_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    cognome = db.Column(db.String(50),nullable=False)
    nome = db.Column(db.String(50),nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)

class lotti(db.Model):
    __tablename__ = LOTTI_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    prodotto_id = db.Column(db.String(80),db.ForeginKey('prodotti.id')) #fk
    data_consegna = db.Column(db.String(80))
    qta_unita_misura = db.Column(db.String(20))
    qta_lotto = db.Column(db.String(100))
    prezzo_unitario=db.Column(db.Integer)
    sospeso = db.Column(db.String())

class prenotazioni(db.Model):
    __tablename__ = PRENOTAZIONI_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    utente_id= db.Column(db.Integer,db.ForeginKey('users.id')) #fk
    lotto_id = db.Column(db.Integer,db.ForeginKey('lotti.id')) #fk
    qta = db.Column(db.Integer)


class prodotti(db.Model):
    __tablename__ = PRODOTTI_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True, autoincremet=True)
    produttori_id= db.Column(db.Integer,db.ForeginKey('produttori.id'), unique=True) #fk
    nome_prodotto = db.Column(db.String(80))
 

class produttori(db.Model):
    __tablename__ = PRODUTTORI_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    nome_produttore= db.Column(db.String(),unique=True) 
    descrizione = db.Column(db.Text(),nullable=False) 
    indirizzo = db.Column(db.Text(),nullable=False)
    telefono = db.Column(db.Text(),nullable=False)
    email = db.Column(db.String(), nullable = False)






def init_db(app):
    """
    Funzione per inizializzare il database e popolare le tabelle con i dati
    presenti nei file CSV.
    :param app: Applicazione Flask corrente (per accedere al logger)
    """

    # Crea le tabelle nel database, se queste non esistono già
    db.create_all()

    # Se la tabella NON è già popolata
    if not users.query.first():
        # Se il file CSV esiste
        if os.path.exists(USERS_TABLE_CSV):
            # Apre il file CSV in lettura
            with open(USERS_TABLE_CSV, 'r') as csv_file:
                # Legge il file CSV come dizionario
                csv_reader = csv.DictReader(csv_file)
                # Per ogni riga del file CSV
                for row in csv_reader:
                    # Crea un oggetto User con i valori della riga corrente
                    new_record = users(
                        cognome=row['cognome'],
                        nome=row['nome'],
                        telefono=row['telefono'],
                        email=row['email'],
                        password = row['password']
                    )
                    # Aggiunge l'oggetto User al database
                    db.session.add(new_record)
                # Conferma le modifiche al database
                db.session.commit()
                app.logger.info(f'Tabella "{USERS_TABLE_NAME}" popolata correttamente.')
        else:
            app.logger.error(
                f'Il file "{USERS_TABLE_CSV}" non esiste. '
                'Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{USERS_TABLE_NAME}" già popolata.')

    # Idem come sopra, ma per la tabella lotti
    if not lotti.query.first():
        if os.path.exists(LOTTI_TABLE_CSV):
            with open(LOTTI_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    new_record = lotti(
                        prodotto_id=row['prodotto_id'],
                        data_consegna=row['data_consegna'],
                        qta_unita_misura = row['qta_unita_misura'],
                        qta_lotto=row['qta_lotto'],
                        prezzo_unitario=row['prezzo_unitario'],
                        sospeso = row['sospeso'],
                    )
                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella "{LOTTI_TABLE_NAME}" popolata correttamente.')
        else:
            app.logger.error(
               f'Il file "{LOTTI_TABLE_CSV}" non esiste. '
               'Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{LOTTI_TABLE_NAME}" già popolata.')

           # Idem come sopra, ma per la tabella prenottazioni
    if not prenotazioni.query.first():
        if os.path.exists(PRENOTAZIONI_TABLE_CSV):
            with open(PRENOTAZIONI_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    new_record = prenotazioni(
                        utente_id=row['utente_id'],
                        lotto_id=row['lotto_id'],
                        qta = row['qta'],
                    )
                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella "{PRENOTAZIONI_TABLE_NAME}" popolata correttamente.')
        else:
            app.logger.error(
               f'Il file "{PRENOTAZIONI_TABLE_CSV}" non esiste. '
               'Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{PRENOTAZIONI_TABLE_NAME}" già popolata.')



     # Idem come sopra, ma per la tabella prodotti
    if not prodotti.query.first():
        if os.path.exists(PRODOTTI_TABLE_CSV):
            with open(PRODOTTI_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    new_record = prodotti(
                        produttore_id=row['produttore_id'],
                        nome_prodotto=row['nome_prodotto'],
                    )
                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella "{PRODOTTI_TABLE_NAME}" popolata correttamente.')
        else:
            app.logger.error(
               f'Il file "{PRODOTTI_TABLE_CSV}" non esiste. '
               'Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{PRODOTTI_TABLE_NAME}" già popolata.')



         # Idem come sopra, ma per la tabella produttori
    if not produttori.query.first():
        if os.path.exists(PRODUTTORI_TABLE_CSV):
            with open(PRODUTTORI_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    new_record = produttori(
                        nome_produttore=row['nome_produttore'],
                        descrizione=row['descrizione'],
                        indirizzo=row['indirizzo'],
                        telefono=row['telefono'],
                        email =row['email']
                    )
                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella "{PRODUTTORI_TABLE_NAME}" popolata correttamente.')
        else:
            app.logger.error(
               f'Il file "{PRODUTTORI_TABLE_CSV}" non esiste. '
               'Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{PRODUTTORI_TABLE_NAME}" già popolata.')