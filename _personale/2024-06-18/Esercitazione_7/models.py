import csv
from datetime import datetime
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from settings import USER_TABLE_NAME, FILM_TABLE_NAME, USER_TABLE_CSV, FILM_TABLE_CSV

db = SQLAlchemy()

# definire le tabelle
class User(db.Model):
    __tablename__ = USER_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    nome = db.Column(db.String(80))
    cognome = db.Column(db.String(80))
    indirizzo = db.Column(db.String(120))
    citta = db.Column(db.String(80))
    tel1 = db.Column(db.String(80))
    tel2 = db.Column(db.String(80))
    email = db.Column(db.String(80))
    datanascita = db.Column(db.Date)
    datareg = db.Column(db.Date)

class Film(db.Model):
    __tablename__ = FILM_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String, nullable=False)

def init_db(app): 
    db.create_all()

    if not User.query.first():
        if os.path.exists(USER_TABLE_CSV):
            with open(USER_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    new_record = User(
                        login = row['LOGIN'],
                        password = row['PASSWORD'],
                        nome = row['NOME'],
                        cognome = row['COGNOME'],
                        indirizzo = row['INDIRIZZO'],
                        citta = row['CITTA'],
                        tel1 = row['TEL1'],
                        tel2 = row['TEL2'],
                        email = row['EMAIL'],
                        datanascita=datetime.strptime(row['DATANASCITA'], '%Y-%m-%d'),
                        datareg=datetime.strptime(row['DATAREG'], '%Y-%m-%d')
                    )

                    db.session.add(new_record)
                
            db.session.commit()
            app.logger.info(f'Tabella "{USER_TABLE_NAME}" aggiornata correttamente.')
        else:
            app.logger.error(
                f'Il file "{USER_TABLE_CSV}" non esiste. '
                'Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{USER_TABLE_NAME}" già aggiornata.')

    if not Film.query.first():
        if os.path.exists(FILM_TABLE_CSV):
            with open(FILM_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    new_record = Film(
                        title = row['TITLE'],
                        image = row['IMAGE']
                    )

                    db.session.add(new_record)
                
            db.session.commit()
            app.logger.info(f'Tabella "{FILM_TABLE_NAME}" aggiornata correttamente.')
        else:
            app.logger.error(
                f'Il file "{FILM_TABLE_CSV}" non esiste. '
                'Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{FILM_TABLE_NAME}" già aggiornata.')
                         


    
    