from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
# def tabelle

def int_db(app):

  db.create_all()

  #importare i dati


