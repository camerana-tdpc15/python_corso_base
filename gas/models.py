import json
import os
from flask_sqlalchemy import SQLAlchemy
from settings import BASE_DIR

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    #creazione tabella per verifica
    id = db.Column(db.integer, primary_key =True, autoincrement=True)
    nome = db.Column(db.String(50), nullable =False)  #campi obbligatori
    cognome = db.Column(db.String(50), nullable =False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable =False)
    password = db.Column(db.String(30), nullable =False)

new_user = User(
   nome='Pippo',
   cognome='Pluto'
   email='asd@asd.asd'
   password='cicciopasticcio')

new_user = User({
   nome='Pippo',
   cognome='Pluto'
   email='asd@asd.asd'
   password='cicciopasticcio'
})

new_user = User(**data)
db.session.add(new_user)
db.session.commit()

    class Produttore(db.Model):
        __tablename__ = 'produttori'
    id = db.Column(db.integer, primary_key = True, autoincrement=True)
    nome_produttore = db.Column(db.String(100), unique=True, nullable =False) 
    descrizione = db.Column(db.Text(), nullable =False)
    indirizzo = db.Column(db.Text(), nullable =False)
    telefono = db.Column(db.String(20), nullable =False)
    email = db.Column(db.String(50), nullable =False)



    class Prodotto(db.Model):
     __tablename__ = 'prodotti'
    id = db.Column(db.integer, primary_key = True, autoincrement =True)
    Produttore_id =  db.Column(db.integer, db.ForeginKey('produttori.id') nullable =False)
    nome_prodotto =  db.Column(db.String(50), nullable =False)



    class Lotto(db.Model):
    __tablename__ = 'lotti' 
    id = db.Column(db.integer, primary_key = True, autoincrement=True)
    prodotto_id = db.Column(db.integer db.ForeginKey('prodotti.id'), nullable =False) 
    data_consegna = db.Column(db.Date)
    qta_unita_misura = db.Column(db.TString(10), nullable =False)
    qta_lotto = db.Column(db.Integer, nullable =False)
    prezzo_unitario= db.Column(db.Float, nullable =False)  
    sospeso = db.Column(db.boolean, default=False)



    class Prenotazione (db.Model):
       __tablename__ = 'prenotazioni'
    id = db.Column(db.integer, primary_key = True, autoincrement =True)
    lotto_id=  db.Column(db.integer, db.ForeginKey('lotti.id') nullable =False)
    user_id =  db.Column(db.Integer,db.ForeginKey('user.id') nullable =False)
       



def init_db():
   # crea le tabelle se non esistono già    
       db.create_all()

    #popolo le tabelle con i dati se non esiste un record in user
       if User.query.first() is None:
           
          
        json_files = [
       ('lotti.json', Lotto),
       'prenotazioni.json',
       'prodotti.json',
       'produttori.json',
       'user.json',

        ]


        for filename in json_files:
            file_path = os.path.join(BASE_DIR, 'database', 'data_json', filename)
            print(file_path)

            with open (file_path, 'r') as file:
               lista_record = json.load(file)

               for record_dict in lista_record:
                  new_record = model(**record_dict)
                  db.session.add(new_record)
