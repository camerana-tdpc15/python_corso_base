import locale
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

locale.setlocale(locale.LC_TIME, 'it_IT')

db = SQLAlchemy()  
class Utente(db.Model, SerializerMixin):
    __tablename__ = 'utenti' 
    id = db.mapped_column(db.Integer(), primary_key=True)
    cognome =db.mapped_column(db.String(50), nullable = False)
    nome =db.mapped_column(db.String(50), nullable = False)
    telefono =db.mapped_column(db.String(20), nullable = False)
    email =db.mapped_column(db.String(50), unique =True, nullable = False)
    password =db.mapped_column(db.String(30), nullable = False)

class Prenotazione(db.Model, SerializerMixin):
    __tablename__= 'prenotazioni'
    id = db.mapped_column(db.Integer(), primary_key = True)
    utente_id = db.mapped_column(db.Integer(), db.ForignKey('utenti.id'), nullable = False)
    replica_id = db.mapped_column(db.Integer(), db.ForeignKey('repliche.id'), nullable = False)


class Replica(db.Models, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.mapped_column(db.Integer(), primary_key=True)
    evento_id = db.mapped_column(db.Integer(), db.ForignKey('eventi.id'), nullable = False)
    data_ora = db.mapped_column(db.Datetime(), nullable=False)
    annulato = db.mapped_column(db.Boolean(), default=False)

class Evento(db.Model, SerializerMixin):
    _tablename__='eventi'
    id = db.mapped_column(db.Integer(), primary_key=True)
    locale_id = db.mapped_column(db.Integer(), db.ForignKey('locali.id'), nullable = False)
    nome_evento = db.mapped_column(db.String(50), nullable = False)

class Locale(db.Models, SerializerMixin):
    __tablemane__ = 'locali'
    id = db.mapped_column(db.Integer(), primary_key=True)
    nome_locale = db.mapped_column(db.String(50), nullable = False)
    luogo = db.mapped_column(db.String(100), nullable = False)
    posti = db.mapped_column(db.Integer(), nullable = False)

    serialize_rules = ('get_posti_disponibili', 'get_date', 'get_elenco_eventi')

    # def get_posti_disponibili(self):
    #     posti_disponibili = Locale.query.filter_by(posti=self.id).all()
    #     posti_prenotati = sum()

    def get_posti_disponibili(self):
        prenotazioni_replica = Prenotazione.query.filter_by(Replica_id=self.id).all()
        posti_prenotati = sum(prenotazione.qta for prenotazione in prenotazioni_replica)
        return self.posti - posti_prenotati
    


