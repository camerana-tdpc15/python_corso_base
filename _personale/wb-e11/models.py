import csv
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from settings import  LOTTI_TABLE_NAME,PRENOTAZONI_TABLE_NAME,PRODOTTI_TABLE_NAME,PRODUTTORI_TABLE_NAME,USERS_TABLE_NAME,LOTTI_TABLE_CSV,PRENOTAZONI_TABLE_CSV,PRODOTTI_TABLE_CSV,PRODUTTORI_TABLE_CSV,USERS_TABLE_CSV


db=SQLAlchemy()

class lotti(db.Model):
    __tablename__=LOTTI_TABLE_NAME
    id= db.Column(db.Integer, primary_key=True)
    prodotto_id= db.Column(db.Integer) #FK
    data_consegna= db.Column(db.Date)
    qta_unita_misura= db.Column(db.Integer)
    qta_lotto=db.Column(db.Integer)
    prezzo_unitario= db.Column(db.Integer)
    sospeso = db.Column(db.Integer)

class users(db.Model):
    __tablename__=USERS_TABLE_NAME
    id=db.Column(db.Integer, primary_key=True)
    cognome=db.Column(db.String(80))
    nome=db.Column(db.String(80))
    telefono=db.Column(db.String(80))
    email=db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(80), nullable=False)


class prodotti(db.Model):
        __tablename__=PRODOTTI_TABLE_NAME
        id=db.Column(db.Integer, primary_key=True)
        produttore_id=db.Column(db.Integer) #FK
        nome_prodotto=db.Column(db.String(20))


class produttori(db.Model):
    __tablename__=PRODUTTORI_TABLE_NAME
    id=db.Column(db.Integer, primary_key=True)
    nome_produttore=db.Column(db.String(30))
    descrizione=db.Column(db.String(80))
    indirizzo= db.Column(db.String(40))
    tel=db.Column(db.String(20))
    email=db.Column(db.String(30))



class prenotazioni(db.Model):
    __tablename__=PRENOTAZONI_TABLE_NAME
    id=db.Column(db.Integer, primary_key=True)
    utente_id=db.Column(db.Integer) #FK users
    lotto_id=db.Column(db.Integer) #FK Lotti
    qta= db.Column(db.Integer)




def init_db(app):
     
    db.create_all()



    if not users.query.first():
        if os.path.exists(USERS_TABLE_CSV):
             with open(USERS_TABLE_CSV,'r')as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                        new_record= users(
                            cognome=row['cognome'],
                            nome=row['nome'],
                            telefono=row['telefono'],
                            email=row['email'],
                            password=row['password'],
                        )
                        db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'Tabella"{USERS_TABLE_NAME}"popolata correttamenente')
        else:
             app.logger.error(
                  f'Il file"{USERS_TABLE_CSV}" non essiste.' 
                  'Verifica il percroso e riprova.')
             sys.exit(1)
    else:
         app.logger.info(f'Tabella"{USERS_TABLE_CSV}" gia popolata')


    if not lotti.query.first():
         
        if os.path.exists(LOTTI_TABLE_CSV):
              
            with open(LOTTI_TABLE_CSV,'r') as csv_file:
                   
                   csv_reader = csv.DictReader(csv_file)

                   for row in csv_reader:
                        
                        new_record= lotti(
                             prodotto_id = row['prodotto_id'],
                             data_consegna = row['data_consegna'],
                             qta_unita_misura=row['qta_unita_misura'],
                             qta_lotto= row['qta_lotto'],
                             prezzo_unitario = row['prezzo_unitario'],
                             sospeso = row['sospeso'],
                        )
                        db.session.add(new_record)

            db.session.commit()
            app.logger.info(f'Tabella"{LOTTI_TABLE_NAME}" popolata correttamente')
        else:
             app.logger.error(
                  f'Il file "{LOTTI_TABLE_CSV}" non esiste.'
                  'Verifica il percorso e riprova.'
             )
             sys.exit(1)
    else:
         app.logger.info(f'Tabella"{LOTTI_TABLE_CSV}" gia popolata.')

    


    if not prodotti.query.first():
         
        if os.path.exists(PRODOTTI_TABLE_CSV):
              
            with open(PRODOTTI_TABLE_CSV,'r') as csv_file:
                   
                   csv_reader = csv.DictReader(csv_file)

                   for row in csv_reader:
                        
                        new_record= prodotti(
                            produttore_id =row ['PRODUTTE_ID'],
                            nome_prodotto=row['NOME_PRODOTTO']
                        )
                        db.session.add(new_record)

            db.session.commit()
            app.logger.info(f'Tabella"{PRODOTTI_TABLE_NAME}" popolata correttamente')
        else:
             app.logger.error(
                  f'Il file "{PRODOTTI_TABLE_CSV}" non esiste.'
                  'Verifica il percorso e riprova.'
             )
             sys.exit(1)
    else:
         app.logger.info(f'Tabella"{PRODOTTI_TABLE_CSV}" gia popolata.')





    if not produttori.query.firts():
     
        if os.path.exists(PRODUTTORI_TABLE_CSV):
          
            with open(PRODUTTORI_TABLE_CSV,'r') as csv_file:
               csv_reader = csv.DictReader(csv_file)

               for row in csv_reader:
                    new_record=produttori(
                        
                        nome_produttore=row['NOME_PRODUTTORE'],
                        descrizione=row['DESCRIZIONE'],
                        indirizzo=row['INDIRIZZO'],
                        tel=row['TEL'],
                        email=row['EMAIL'],
                    )
                    db.session.add(new_record)

            db.session.commit()
            app.logger.info(f'Tabella "{PRODUTTORI_TABLE_CSV}" popolata correttamente')
        
        else:
             app.logger.error(
                  f'Il file"{PRODUTTORI_TABLE_CSV}" non esiste.'
                  'Verifica il percorso e riprova'
             )
             sys.exit(1)
    else:
        app.logger.info(f'Tabella"{PRODUTTORI_TABLE_CSV}"gia popolata')





    if not prenotazioni.query.first():
         
        if os.path.exists(PRENOTAZONI_TABLE_CSV):
             
            with open(PRENOTAZONI_TABLE_CSV,'r') as csv_file:
                 
                csv_reader = csv.DictReader(csv_file)

                for row in csv_reader:
                    new_record=prenotazioni(
                        utente_id=row['UTENTE_ID'],
                        lotto_id=row['LOTTO_ID'],
                        qta=row['QTA'],
                    )
                    db.session.add(new_record)
                db.session.commit()
                app.logger.info(f'tabella "{PRENOTAZONI_TABLE_CSV}" popolata correttamente')
        else:
             app.logger.error(
                  f'Il file"{PRENOTAZONI_TABLE_CSV}"non esiste.'
                  'Verifica il percorso e riprova'
             )
             sys.exit(1)
    else:
         app.logger.info(f'Tabella"{PRENOTAZONI_TABLE_CSV}" gia popolata')