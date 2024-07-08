from flask_sqlalchemy import SQLAlchemy
from settings import BASE_DIR_PATH
import os , json
from pprint import pprint
from datetime import date 
from sqlalchemy_serializer import SerializerMixin
db = SQLAlchemy()

class User(db.Model,SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

class Produttore(db.Model,SerializerMixin):
    __tablename__ = 'produttori'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produttore = db.Column(db.String(), unique=True, nullable=False)
    descrizione = db.Column(db.Text(), nullable=False)
    indirizzo = db.Column(db.Text(), nullable=False)
    telefono = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
# RELATIONSHIPS
    rel_prodotti = db.relationship('Prodotto', back_populates='rel_produttore')

    serialize_rules = ('-rel_prodotti.rel_produttore',)

class Prodotto(db.Model,SerializerMixin):
    __tablename__ = 'prodotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttori.id'), nullable=False)
    nome_prodotto = db.Column(db.String(50), nullable=False)
  # RELATIONSHIPS
    rel_lotti = db.relationship('Lotto', back_populates='rel_prodotto')
    rel_produttore = db.relationship('Produttore', back_populates='rel_prodotti')

    serialize_rules = ('-rel_lotti.rel_prodotto', '-rel_produttore.rel_prodotti')
class Lotto(db.Model,SerializerMixin):
    __tablename__ = 'lotti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean, default=False)
      # RELATIONSHIPS
    rel_prodotto = db.relationship('Prodotto', back_populates='rel_lotti')
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_lotto')

    serialize_rules = ('-rel_prodotto.rel_lotti', '-rel_prenotazioni.rel_lotto', 'get_date', 'get_prezzo_str', 'get_qta_disponibile')


    def get_date(self):
        return_data= self.data_consegna.strftime('%A %d/%m/%Y')
        return return_data
    
    def get_prezzo_str(self):
        return f'{self.prezzo_unitario} €/{self.qta_unita_misura}'
    
    def get_qta_disponibile(self):
        qta_prenotate= 0
        for prenot in self.rel_prenotazioni:
            qta_prenotate += prenot.qta
        qta_disponibile = self.qta_lotto - qta_prenotate
        return qta_disponibile


class Prenotazione(db.Model,SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotti.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    qta = db.Column(db.Integer, nullable=False)
     # RELATIONSHIPS
    rel_lotto = db.relationship('Lotto', back_populates='rel_prenotazioni')

    serialize_rules = ('-rel_lotto.rel_prenotazioni',)

    # Da implementare l'unique constraint per la coppia lotto_id e user_id
    
    __table_args__ = (
        db.UniqueConstraint('lotto_id', 'user_id', name='unica_prenotazione'),
    )


def init_db():
    # Crea le tabelle se non esistono già
    db.create_all()
 #Inserisco dati nuovo user nella tabella User
   # new_user = User(**{ 
   #     'nome' : 'Pippo',
   #     'cognome' :'Pluto',
   #     'email' :'asd@asd.com',
   #     'password' :'asdasdasd',
   # })
   # db.session.add(new_user)
   # db.session.commit() 


    # Popolo le tabelle con i dati se non esiste il record nella prima tabella
    if User.query.first() is None:
        
        json_files = [          
           ('users.json',User),
           ('produttori.json',Produttore),
           ('prenotazioni.json',Prenotazione),
           ('prodotti.json',Prodotto),
           ('lotti.json',Lotto),
        ]
    #Scrivo il percorso di ogni file
        for file_name,model in json_files:
            file_path = os.path.join(BASE_DIR_PATH,'database','data_json',file_name)
    #Apro il file json e lo traformo in un file python (dizionario)
            with open(file_path,'r') as jsonfile:
                dict_from_json = json.load(jsonfile)
                #quando la chiave è 'data_consegna' trasforma la data in formato datetime dal formato iso e lo sovrascive
            for record in dict_from_json:
                if 'data_consegna' in record:
                    record['data_consegna'] = date.fromisoformat(record['data_consegna'])

    #per ogni dizionario inserisco la chiave e il valore nella tabella utilizzando il metodo **
                new_record = model(**record )
                db.session.add(new_record)

        db.session.commit() 


