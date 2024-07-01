from flask_sqlalchemy import SQLAlchemy

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
    user_id = db.column(db.Integer, db.ForeignKey('users.id'), )
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)    
    qta = db.Column(db.Integer, nullable=False)


    # creo la funzione che inizializza il db, ma NON LA USO
    def init_db(app):

        
            # crea il db con tutte le tabelle
            db.create_all()