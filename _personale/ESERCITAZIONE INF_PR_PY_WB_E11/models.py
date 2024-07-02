from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()





def init_db():
    # Crea le tabelle se non esistono già
    db.create_all()

    # Popolo le tabelle con i dati
    ...