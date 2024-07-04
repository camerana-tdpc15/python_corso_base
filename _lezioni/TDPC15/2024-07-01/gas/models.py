from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

class User (db.Model):
    __tabelname__ = 'Users'
    id= db.Column(db.Integer, primary_key= True, autoincrement= True)
    nome = db.Column(db.String(50), nullable= False)
    cognome = db.Column(db.String(50), nullable= False)
    telefono = db.column(db.String(20))
    email = db.column(db.String(50), unique=True, nullable= False)
    password = db.Column(db.String(30), nullable= False)

class Produttore (db.Model):  
    __tabelname__ = 'Produttori'
    id= db.Column(db.Integer, primary_key= True, autoincrement= True)
    nome_produttore = db.Column(db.String(50), unique= True, nullable=False)
    descrizione = db.Column(db.text(50), nullable= False)
    indirizzo = db.column(db.text(20), nullable= False)
    telefono = db.column(db.string(50), unique=True, nullable= False)
    email = db.Column(db.string(30), nullable= False) 

class Prodotto (db.Model):  
    __tabelname__ = 'Prodotti'
    id= db.Column(db.Integer, primary_key= True, autoincrement= True)
    produttore_id = db.Column(db.integer, db.ForeginKey('Produttori.id'), nullable=False)
    nome_prodotto = db.Column(db.text(50), nullable= False)
    
class Lotto(db.Model):
   __tabelname__ = 'Lotti'
   id= db.Column(db.Integer, primary_key= True, autoincrement= True)
   prodotto_id = db.Column(db.integer, db.ForeginKey('Prodotti.id'), nullable=False)
   data_consegna = db.Column(db.Date)
   qta_unita_misura = db.Column(db.String(10))
   qta_lotto = db.column(db.Integer)
   prezzo_unitario = db.Column (db.Float, nullable = False)
   sospeso = db.Column( db.Boolean, default= False)

class Prenotazioni(db.Model):
    __tabelname__ = 'Prenotazione'
    id= db.Column(db.Integer, primary_key= True, autoincrement= True)
    lotto_id = db.Column(db.Integer, db.ForeginKey('Lotti.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeginKey('Users.id'), nullable=False)
    qta = db.column (db.Integer, nullable= False)

def init_db(app):

    with app.app_context():
        db.create_all()    