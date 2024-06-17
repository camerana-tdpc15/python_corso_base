import csv
import os
import sys
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from settings import USER_TABLE_NAME, FILM_TABLE_NAME, USER_TABLE_CSV, FILM_TABLE_CSV

db = SQLAlchemy()  # Crea l'istanza di SQLAlchemy

class User(db.Model):
    __tablename__ = USER_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    nome = db.Column(db.String(80))
    cognome = db.Column(db.String(80))
    indirizzo = db.Column(db.String(120))
    citta = db.Column(db.String(80))
    tel1 = db.Column(db.String(20))
    tel2 = db.Column(db.String(20))
    email = db.Column(db.String(100))
    data_nascita = db.Column(db.Date)
    data_reg = db.Column(db.Date)


class Film(db.Model):
    __tablename__ = FILM_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(80), nullable=False)


def init_db(app):
    """
    Funzione per inizializzare il database e popolare le tabelle con i dati
    presenti nei file CSV.
    :param app: Applicazione Flask corrente (per accedere al logger)
    """

    # Crea le tabelle nel database, se queste non esistono già
    db.create_all()

    # Se la tabella NON è già popolata
    if not User.query.first():
        # Se il file CSV esiste
        if os.path.exists(USER_TABLE_CSV):
            # Apre il file CSV in lettura
            with open(USER_TABLE_CSV, 'r') as csv_file:
                # Legge il file CSV come dizionario
                csv_reader = csv.DictReader(csv_file)
                # Per ogni riga del file CSV
                for row in csv_reader:
                    # Crea un oggetto User con i valori della riga corrente
                    new_record = User(
                        login=row['LOGIN'],
                        password=row['PASSWORD'],
                        nome=row['NOME'],
                        cognome=row['COGNOME'],
                        indirizzo=row['INDIRIZZO'],
                        citta=row['CITTA'],
                        tel1=row['TEL1'],
                        tel2=row['TEL2'],
                        email=row['EMAIL'],
                        data_nascita=datetime.strptime(row['DATANASCITA'], '%Y-%m-%d'),
                        data_reg=datetime.strptime(row['DATAREG'], '%Y-%m-%d')
                    )
                    # Aggiunge l'oggetto User al database
                    db.session.add(new_record)
                # Conferma le modifiche al database
                db.session.commit()
                app.logger.info(f'Tabella "{USER_TABLE_NAME}" popolata correttamente.')
        else:
            app.logger.error(
                f'Il file "{USER_TABLE_CSV}" non esiste. '
                'Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{USER_TABLE_NAME}" già popolata.')

    # Idem come sopra, ma per la tabella Film
    if not Film.query.first():
        if os.path.exists(FILM_TABLE_CSV):
            with open(FILM_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    new_record = Film(
                        title=row['TITLE'],
                        image=row['IMAGE'],
                    )
                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella "{FILM_TABLE_NAME}" popolata correttamente.')
        else:
            app.logger.error(
               f'Il file "{USER_TABLE_CSV}" non esiste. '
               'Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{FILM_TABLE_NAME}" già popolata.')