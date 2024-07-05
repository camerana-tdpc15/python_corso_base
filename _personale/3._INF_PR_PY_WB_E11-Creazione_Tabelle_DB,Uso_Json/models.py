import os, json
from pprint import pprint
from datetime import date

from flask_sqlalchemy import SQLAlchemy

from settings import BASE_DIR_PATH

# configuro SQLAlchemy per la gestione del db
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
  
   
    # controllo se la tabella user è vuota
    if User.query.first() is None:
        
        # Definisce una lista di tuple, 
        # dove ogni tupla contiene il nome di un file JSON e la corrispondente classe del modello.
        json_files = [           
            ('lotti.json', Lotto),
            ('prenotazioni.json',Prenotazione), 
            ('prodotti.json',Prodotto),
            ('produttori.json',Produttore),
            ('users.json',User),
        ]

        # con ciclo FOR per ogni file JSON nella lista
        for file_name, model in json_files:
            
            # Costruisce il percorso del file.
            file_path = os.path.join(BASE_DIR_PATH, 'database','data_json', file_name)
            
            # stampo il file_path
            print(file_path)
            
            # apro e leggo il file json
            with open(file_path, 'r')as json_file:

                # caricandone i dati in lista_record
                lista_record = json.load(json_file)

                # faccio ciclo for per prendere un record alla volta
                for record_dict in lista_record:
                    
                    # se il record contiene una data (data_consegna), 
                    if 'data_consegna' in record_dict:
                        
                        # converte la stringa ISO in un oggetto date.
                        var_data_consegna = date.fromisoformat(record_dict['data_consegna'])                        
                        record_dict['data_consegna'] = var_data_consegna 


                    # creo un nuovo oggetto
                    new_record = model(**record_dict)
                    
                    # Aggiunge il nuovo record alla sessione del database.
                    db.session.add(new_record)
         
        # salvo            
        db.session.commit()


               
