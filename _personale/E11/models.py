from flask_sqlalchemy import SQLAlchemy
import os
import csv
import sys
from settings import USERS_FILE_PATH,LOTTI_FILE_PATH,PRODUTTORI_FILE_PATH,PRODOTTI_FILE_PATH,PRENOTAZIONI_FILE_PATH

db = SQLAlchemy()  # Crea l'istanza di SQLAlchemy


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

class Produttore(db.Model):
    __tablename__ = 'produttori'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produttore = db.Column(db.String(), unique=True, nullable=False)
    descrizione = db.Column(db.Text(), nullable=False)
    indirizzo = db.Column(db.Text(), nullable=False)
    telefono = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)


class Prodotto(db.Model):
    __tablename__ = 'prodotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), nullable=False)
    nome_prodotto = db.Column(db.String(50), nullable=False)

class Lotto(db.Model):
    __tablename__ = 'lotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, default=False)

class Prenotazione(db.Model):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)




def init_db(app):
    # Crea le tabelle se non esistono già
    db.create_all()
   
    if not User.query.first():

        if os.path.exists(USERS_FILE_PATH):

            with open(USERS_FILE_PATH,'r') as csv_file:

                csv_reader= csv.DictReader(csv_file)

                for row  in csv_reader:

                    new_record= User(
                        nome=row['nome'],
                        cognome=row['cognome'],
                        telefono=row['telefono'],
                        email=row['email'],
                        password=row['password'],
                    )

                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella {USERS_FILE_PATH} popolata correttamente')
        else:
            app.logger.error(f'Tabella {USERS_FILE_PATH} non esiste, Verifica il percorso e riprova')
            sys.exit(1)
    else:
        app.logger.info(f'Tabella {USERS_FILE_PATH} già popolata.')
        

    if not User.query.first():

        if os.path.exists(LOTTI_FILE_PATH):

            with open(LOTTI_FILE_PATH,'r') as csv_file:

                csv_reader= csv.DictReader(csv_file)

                for row  in csv_reader:

                    new_record= Lotto(
                        prodotto_id=row['prodotto_id'],
                        data_consegna=row['data_consegna'],
                        qta_unita_misura=row['qta_unita_misura'],
                        qta_lotto=row['qta_lotto'],
                        prezzo_unitario=row['prezzo_unitario'],
                        sospeso=row['sospeso'],
                    )

                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella {LOTTI_FILE_PATH} popolata correttamente')
        else:
            app.logger.error(f'Tabella {LOTTI_FILE_PATH} non esiste, Verifica il percorso e riprova')
            sys.exit(1)
    else:
        app.logger.info(f'Tabella {LOTTI_FILE_PATH} già popolata.')
    
    
    if not User.query.first():

        if os.path.exists(PRODUTTORI_FILE_PATH):

            with open(PRODUTTORI_FILE_PATH,'r') as csv_file:

                csv_reader= csv.DictReader(csv_file)

                for row  in csv_reader:

                    new_record= Produttore(
                        nome_produttore=row['nome_produttore'],
                        descrizione=row['descrizione'],
                        indirizzo=row['indirizzo'],
                        telefono=row['telefono'],
                        email=row['email']
                    )

                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella {PRODUTTORI_FILE_PATH} popolata correttamente')
        else:
            app.logger.error(f'Tabella {PRODUTTORI_FILE_PATH} non esiste, Verifica il percorso e riprova')
            sys.exit(1)
    else:
        app.logger.info(f'Tabella {PRODUTTORI_FILE_PATH} già popolata.')
        

    if not User.query.first():

        if os.path.exists(PRODOTTI_FILE_PATH):

            with open(PRODOTTI_FILE_PATH,'r') as csv_file:

                csv_reader= csv.DictReader(csv_file)

                for row  in csv_reader:

                    new_record= Prodotto(
                        produttore_id=row['produttore_id'],
                        nome_prodotto=row['nome_prodotto'],
                    )

                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella {PRODOTTI_FILE_PATH} popolata correttamente')
        else:
            app.logger.error(f'Tabella {PRODOTTI_FILE_PATH} non esiste, Verifica il percorso e riprova')
            sys.exit(1)
    else:
        app.logger.info(f'Tabella {PRODOTTI_FILE_PATH} già popolata.')


    if not User.query.first():

        if os.path.exists(PRENOTAZIONI_FILE_PATH):

            with open(PRENOTAZIONI_FILE_PATH,'r') as csv_file:

                csv_reader= csv.DictReader(csv_file)

                for row  in csv_reader:

                    new_record= Prenotazione(
                        utente_id=row['utente_id'],
                        lotto_id=row['lotto_id'],
                        qta=row['qta']
                    )

                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella {PRENOTAZIONI_FILE_PATH} popolata correttamente')
        else:
            app.logger.error(f'Tabella {PRENOTAZIONI_FILE_PATH} non esiste, Verifica il percorso e riprova')
            sys.exit(1)
    else:
        app.logger.info(f'Tabella {PRENOTAZIONI_FILE_PATH} già popolata.')