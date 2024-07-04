import os, json
from pprint import pprint
from datetime import date

from flask_sqlalchemy import SQLAlchemy

from settings import BASE_DIR_PATH

db = SQLAlchemy()

# creo tabella USERS
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)


    
    
# creo tabella PRODUTTORI
class Produttore(db.Model):
    __tablename__ = 'produttori'
    id = db.Column(db.Integer, primary_key=True)
    nome_produttore = db.Column(db.String(100), nullable=False, unique=True)
    descrizione = db.Column(db.Text)
    indirizzo = db.Column(db.Text, )
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)

# creo tabella PRODOTTI    
class Prodotto(db.Model):
    __tablename__ = 'prodotti'
    id = db.Column(db.Integer, primary_key=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), nullable=False)
    nome_prodotto = db.Column(db.String(50), nullable=False)

# creo tabella LOTTI    
class Lotto(db.Model):
    __tablename__ = 'lotti'
    id = db.Column(db.Integer, primary_key=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.Column(db.DateTime, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, default=False)
    
# creo tabella PRENOTAZIONI
class Prenotazione(db.Model):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), )
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)    
    qta = db.Column(db.Integer, nullable=False)


# creo la funzione che inizializza il db, ma NON LA USO
def init_db(app):

    # crea il db con tutte le tabelle
    db.create_all()
  
   
    # così controllo se la tabella user è gia popolata 
    if User.query.first() is None:
        # tiro fuori la lista dei file json
        json_files = [
            # per utilità oltre ai file eassocio anche i nomi delle tabelle
            ('lotti.json', Lotto),
            ('prenotazioni.json',Prenotazione), 
            ('prodotti.json',Prodotto),
            ('produttori.json',Produttore),
            ('users.json',User),
        ]

        # con ciclo FOR mi tiro fuori il path di ogni file 
        for file_name, model in json_files:
            file_path = os.path.join(BASE_DIR_PATH, 'database','data_json', file_name)
            
            print(file_path)
            # apro e leggo il file json
            with open(file_path, 'r')as json_file:

                # creo dizionario dal file json
                lista_record = json.load(json_file)

                # faccio ciclo for per prendere un record alla volta
                for record_dict in lista_record:

                    if 'data_consegna' in record_dict:
                        var_data_consegna = date.fromisoformat(record_dict['data_consegna'])
                        record_dict['data_consegna'] = var_data_consegna 


                    # creo un nuovo modello
                    new_record = model(**record_dict)
                    db.session.add(new_record)
        db.session.commit()


               
