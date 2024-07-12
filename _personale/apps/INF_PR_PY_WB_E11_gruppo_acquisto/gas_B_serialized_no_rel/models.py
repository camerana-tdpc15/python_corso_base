import locale
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

locale.setlocale(locale.LC_TIME, 'it_IT')

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.mapped_column(db.Integer(), primary_key=True)
    cognome = db.mapped_column(db.String(50), nullable=False)
    nome = db.mapped_column(db.String(50), nullable=False)
    telefono = db.mapped_column(db.String(20), nullable=False)
    email = db.mapped_column(db.String(50), unique=True, nullable=False)
    password = db.mapped_column(db.String(30), nullable=False)

class Produttore(db.Model, SerializerMixin):
    __tablename__ = 'produttori'
    id = db.mapped_column(db.Integer(), primary_key=True)
    nome = db.mapped_column(db.String(100), nullable=False)
    descrizione = db.mapped_column(db.Text(), nullable=False)
    indirizzo = db.mapped_column(db.Text(), nullable=False)
    telefono = db.mapped_column(db.String(20), nullable=False)
    email = db.mapped_column(db.String(50), nullable=False)

class Prodotto(db.Model, SerializerMixin):
    __tablename__ = 'prodotti'
    id = db.mapped_column(db.Integer(), primary_key=True)
    produttore_id = db.mapped_column(db.Integer(), db.ForeignKey('produttori.id'), nullable=False)
    nome = db.mapped_column(db.String(50), nullable=False)

class Lotto(db.Model, SerializerMixin):
    __tablename__ = 'lotti'
    id = db.mapped_column(db.Integer(), primary_key=True)
    prodotto_id = db.mapped_column(db.Integer(), db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.mapped_column(db.Date(), nullable=False)
    qta_unita_misura = db.mapped_column(db.String(10), nullable=False)
    qta_lotto = db.mapped_column(db.Integer(), nullable=False)
    prezzo_unitario = db.mapped_column(db.Float(), nullable=False)
    sospeso = db.mapped_column(db.Boolean(), default=False)

    serialize_rules = ('get_qta_disponibile', 'get_date', 'get_prezzo_str')

    def get_qta_disponibile(self):
        prenotazioni_lotto = Prenotazione.query.filter_by(lotto_id=self.id).all()
        qta_prenotata = sum(prenotazione.qta for prenotazione in prenotazioni_lotto)
        return self.qta_lotto - qta_prenotata
    
    def get_date(self):
        return self.data_consegna.strftime('%A %d/%m/%Y')
    
    def get_prezzo_str(self):
        return f'{self.prezzo_unitario:.2f} €/{self.qta_unita_misura}'


class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.mapped_column(db.Integer(), primary_key=True)
    user_id = db.mapped_column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    lotto_id = db.mapped_column(db.Integer(), db.ForeignKey('lotti.id'), nullable=False)
    qta = db.mapped_column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'lotto_id', name='user_id_lotto_id_uniq'),
    )
