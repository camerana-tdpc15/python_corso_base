from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class Utente(db.Model, SerializerMixin):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_utenti')

class Prenotazione(db.Model, SerializerMixin):
    __tablename__ = 'prenotazioni'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)
    replica_id = db.Column(db.Integer, db.ForeignKey('repliche.id'), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)

    rel_utenti = db.relationship('Utente', back_populates='rel_prenotazioni')
    rel_repliche = db.relationship('Replica', back_populates='rel_prenotazioni')

class Replica(db.Model, SerializerMixin):
    __tablename__ = 'repliche'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventi.id'), nullable=False)
    data_ora = db.Column(db.DateTime, nullable=False)
    annullato = db.Column(db.Boolean, nullable=False)

    rel_eventi = db.relationship('Evento', back_populates='rel_repliche')
    rel_prenotazioni = db.relationship('Prenotazione', back_populates='rel_repliche')

    def get_date(self):
        return self.data_ora.strftime('%A %d/%m/%Y')

    def get_qta_disponibile(self):
        qta_prenotata = sum(prenot.quantita for prenot in self.rel_prenotazioni)
        return self.rel_eventi.rel_locali.posti - qta_prenotata

class Evento(db.Model, SerializerMixin):
    __tablename__ = 'eventi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locale_id = db.Column(db.Integer, db.ForeignKey('locali.id'), nullable=False)
    nome_evento = db.Column(db.String(50), nullable=False)

    rel_locali = db.relationship('Locale', back_populates='rel_eventi')
    rel_repliche = db.relationship('Replica', back_populates='rel_eventi')

class Locale(db.Model, SerializerMixin):
    __tablename__ = 'locali'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_locale = db.Column(db.String(50), nullable=False)
    luogo = db.Column(db.String(100), nullable=False)
    posti = db.Column(db.Integer, nullable=False)

    rel_eventi = db.relationship('Evento', back_populates='rel_locali')


def init_db():
    db.create_all()

    if Utente.query.first() is None:
        json_files = [
            ('eventi.json', Evento),
            ('locali.json', Locale),
            ('prenotazioni.json', Prenotazione),
            ('repliche.json', Replica),
            ('utenti.json', Utente),
        ]

        for filename, model in json_files:
            file_path = os.path.join(BASE_DIR, 'database', 'data_json', filename)

            with open(file_path, 'r') as file:
                lista_record = json.load(file)

            for record_dict in lista_record:
                if 'data_ora' in record_dict:
                    record_dict['data_ora'] = datetime.strptime(record_dict['data_ora'], '%d-%m-%Y-%H:%M:%S')

                new_record = model(**record_dict)
                db.session.add(new_record)

        db.session.commit()
