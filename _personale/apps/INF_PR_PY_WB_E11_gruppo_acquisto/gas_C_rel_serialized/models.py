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
    # -- RELATIONSHIPS --
    prenotazioni = db.relationship('Prenotazione', back_populates='user', lazy='dynamic')

    serialize_rules = ('-prenotazioni.user', '-password')


class Produttore(db.Model, SerializerMixin):
    __tablename__ = 'produttori'
    id = db.mapped_column(db.Integer(), primary_key=True)
    nome = db.mapped_column(db.String(100), nullable=False)
    descrizione = db.mapped_column(db.Text(), nullable=False)
    indirizzo = db.mapped_column(db.Text(), nullable=False)
    telefono = db.mapped_column(db.String(20), nullable=False)
    email = db.mapped_column(db.String(50), nullable=False)
    # -- RELATIONSHIPS --
    prodotti = db.relationship('Prodotto', back_populates='produttore')

    serialize_rules = ('-prodotti.produttore', '-prodotti.lotti.prenotazioni')


class Prodotto(db.Model, SerializerMixin):
    __tablename__ = 'prodotti'
    id = db.mapped_column(db.Integer(), primary_key=True)
    produttore_id = db.mapped_column(db.Integer(), db.ForeignKey('produttori.id'), nullable=False)
    nome = db.mapped_column(db.String(50), nullable=False)
    # -- RELATIONSHIPS --
    produttore = db.relationship('Produttore', back_populates='prodotti')
    lotti = db.relationship('Lotto', back_populates='prodotto')
    
    serialize_rules = ('-produttore.prodotti', '-lotti.prodotto', '-lotti.prenotazioni')


class Lotto(db.Model, SerializerMixin):
    __tablename__ = 'lotti'
    id = db.mapped_column(db.Integer(), primary_key=True)
    prodotto_id = db.mapped_column(db.Integer(), db.ForeignKey('prodotti.id'), nullable=False)
    data_consegna = db.mapped_column(db.Date(), nullable=False)
    qta_unita_misura = db.mapped_column(db.String(10), nullable=False)
    qta_lotto = db.mapped_column(db.Integer(), nullable=False)
    prezzo_unitario = db.mapped_column(db.Float(), nullable=False)
    sospeso = db.mapped_column(db.Boolean(), default=False)
    # -- RELATIONSHIPS --
    prodotto = db.relationship('Prodotto', back_populates='lotti')
    prenotazioni = db.relationship('Prenotazione', back_populates='lotto')

    serialize_rules = ('-prodotto.lotti', '-prenotazioni.lotto', 'get_qta_disponibile', 'get_date', 'get_prezzo_str')

    def get_qta_disponibile(self):
        qta_prenotata = sum(prenotazione.qta for prenotazione in self.prenotazioni)
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
    # -- RELATIONSHIPS --
    user = db.relationship('User', back_populates='prenotazioni')
    lotto = db.relationship('Lotto', back_populates='prenotazioni')  # , order_by='Lotto.data_consegna')

    serialize_rules = ('-user.prenotazioni', '-lotto.prenotazioni', 'get_prezzo_totale_str')


    __table_args__ = (
        db.UniqueConstraint('user_id', 'lotto_id', name='user_id_lotto_id_uniq'),
    )

    @db.validates('qta')
    def validate_qta(self, key, qta):
        if qta <= 0:
            raise ValueError('La quantità deve essere maggiore di zero.')
        
        # Per usare questo, va rivisto lo script di inizializzazione del DB
        # altre_prenotazioni = Prenotazione.query.filter(
        #     Prenotazione.lotto_id == self.lotto_id,
        #     Prenotazione.id != self.id
        # ).all()
        # qta_gia_prenotata = sum(prenotazione.qta for prenotazione in altre_prenotazioni)
        # lotto = db.session.query(Lotto).get(self.lotto_id)
        # if qta_gia_prenotata + qta > lotto.qta_lotto:
        #     raise ValueError('Quantità non disponibile!')

        # lotto = db.session.query(Lotto).get(self.lotto_id)
        # if lotto.sospeso:
        #     raise ValueError('Il lotto è sospeso!')
        
        return qta

    def get_prezzo_totale_str(self):
        prezzo = self.qta * self.lotto.prezzo_unitario
        return f'€ {prezzo:.2f}'