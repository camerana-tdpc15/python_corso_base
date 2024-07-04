import json
import os
import sys
from datetime import datetime
from flask import app
from flask_sqlalchemy import SQLAlchemy
from settings import (
    LOTTI_TABLE_JSON,
    LOTTI_TABLE_NAME,
    PRENOTAZIONI_TABLE_JSON,
    PRENOTAZIONI_TABLE_NAME,
    PRODOTTI_TABLE_JSON,
    PRODOTTI_TABLE_NAME,
    PRODUTTORI_TABLE_JSON,
    PRODUTTORI_TABLE_NAME,
    USERS_TABLE_JSON,
    USERS_TABLE_NAME,
)

db = SQLAlchemy()  # creo istanza SQLAlchemy


# creo la struttura delle tabelle
class User(db.Model):  # nome della classe al singolare e iniziale maiuscola, nome della tabella plurale
    __tablename__ = USERS_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    prenotazioni = db.relationship("Prenotazione", back_populates="utente")


class Produttore(db.Model):
    __tablename__ = PRODUTTORI_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    nome_produttore = db.Column(db.String(150), nullable=False)
    descrizione = db.Column(db.String(250))
    indirizzo = db.Column(db.String(250))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(150))
    prodotti = db.relationship("Prodotto", back_populates="produttore")


class Prodotto(db.Model):
    __tablename__ = PRODOTTI_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    produttore_id = db.Column(
        db.Integer, db.ForeignKey("produttore.id"), nullable=False)
    nome_prodotto = db.Column(db.String(150), nullable=False)
    produttore = db.relationship("Produttore", back_populates="prodotti")
    lotti = db.relationship("Lotto", back_populates="prodotto")


class Lotto(db.Model):
    __tablename__ = LOTTI_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey("prodotto.id"), nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    qta_unita_misura = db.Column(db.String(10), nullable=False)
    qta_lotto = db.Column(db.Integer, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Boolean)
    prodotto = db.relationship("Prodotto", back_populates="lotti")
    prenotazioni = db.relationship("Prenotazione", back_populates="lotto")


class Prenotazione(db.Model):
    __tablename__ = PRENOTAZIONI_TABLE_NAME
    id = db.Column(db.Integer, primary_key=True)
    utente_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lotto_id = db.Column(db.Integer, db.ForeignKey("lotto.id"), nullable=False)
    qta = db.Column(db.Integer, nullable=False)
    utente = db.relationship("User", back_populates="prenotazioni")
    lotto = db.relationship("Lotto", back_populates="prenotazioni")

def init_db(app):
    with app.app_context():  # Attivo il contesto dell'app
        db.create_all()  # Crea tutte le tabelle

        import_data(User, USERS_TABLE_JSON, app)
        import_data(Produttore, PRODUTTORI_TABLE_JSON, app)
        import_data(Prodotto, PRODOTTI_TABLE_JSON, app)
        import_data(Lotto, LOTTI_TABLE_JSON, app, date_fields=["data_consegna"])
        import_data(Prenotazione, PRENOTAZIONI_TABLE_JSON, app)

def import_data(model, file_path, app, date_fields=[]):
    if not model.query.first():
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
                    for item in data:
                        for field in date_fields:
                            item[field] = datetime.strptime(item[field], "%Y-%m-%d")
                        db.session.add(model(**item))
                    db.session.commit()
                    app.logger.info(
                        f'Tabella "{model.__tablename__}" popolata correttamente.'
                    )
            except Exception as e:
                app.logger.error(
                    f'Errore durante la popolazione della tabella "{model.__tablename__}": {e}'
                )
                sys.exit(1)
        else:
            app.logger.error(
                f'Il file "{file_path}" non esiste. Verifica il percorso e riprova.'
            )
            sys.exit(1)
    else:
        app.logger.info(f'Tabella "{model.__tablename__}" già popolata.')