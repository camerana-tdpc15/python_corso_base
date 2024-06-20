import os
import csv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from settings import USER_TABLE_NAME, FILM_TABLE_FILM, USER_TABLE_CSV,FILM_TABLE_CSV

db = SQLAlchemy()
# definire le tabelle
class User(db.Model):
    __tablename__ = USER_TABLE_NAME
    id = db.colum(db.Integer,primary_key = True)
    login=db.colum(db.string(80), unique =True, nulleable = False)
    password = db.colum(db.string(80), nulleable = False)
    nome = db.colum(db.string (80))
    cognome = db.colum(db.string (80))
    indirizzo = db.colum(db.string(80))
    citta = db.colum(db.string(80))
    tel1 = db.colum(db.string(80))
    tel2 = db.colum (db.string(80))
    email = db.colum(db .string(80))
    datanascita = db.colum(db.date)
    datareg = db.colum(db.date)

class Film (db.Model):
    __tablename__ = FILM_TABLE_FILM
    id = db.colum(db.Integer, primary_key = True)
    title = db.colum(db.string(80) nulleable = False)
    image = db.colum(db.string(80) nulleable = False)



def init_db(app):

    db.create_all()

    # importare I dati

    if not User.query.first():

        if os.path.exist(USER_TABLE_CSV):

            with open (USER_TABLE_CSV, 'r') as csv_file:

                csv_reader = csv.DictReader(csv_file)

                for row in csv_file:
                    new_record = User(
                        login= row['LOGIN'],
                        password = row ['PASSWORD'],
                        nome = ['NOME'],
                        cognome = ['COGNOME'],
                        indirizzo = ['INDIRIZZO'],
                        citta = ['CITTA'],
                        tel1 =  ['TEL1']
                        tel2 =  ['TEL2']
                        email = ['EMAIL'],
                        datanascita =,
                        data_reg=datetime.strptime(row['DATAREG'], '%Y-%m-%d')

                    )





