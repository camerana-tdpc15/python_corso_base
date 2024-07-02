import csv
from datetime import datetime
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from settings import STUDENTE_TABLE_CSV,STUDENTE_TABLE_NAME,CORSO_TABLE_CSV,CORSO_TABLE_NAME,DOCENTE_TABLE_CSV,DOCENTE_TABLE_NAME,ESAME_TABLE_CSV,ESAME_TABLE_NAME
db  = SQLAlchemy()

class Studente(db.Model):
    __tablename__ = STUDENTE_TABLE_NAME
    matr_s = db.Column(db.String(80), primary_key=True)
    nome_s = db.Column(db.String(80), nullable=False)
    citta = db.Column(db.String(80), nullable=False)
    

class Docente(db.Model):
    __tablename__ = DOCENTE_TABLE_NAME
    matr_d = db.Column(db.String(80), primary_key=True)
    nome_d = db.Column(db.String(80), nullable=False)

class Corso(db.Model):
    __tablename__ = CORSO_TABLE_NAME
    cod_c = db.Column(db.String(80), primary_key=True)
    nome_c = db.Column(db.String(80), nullable=False)
    matr_d = db.Column(db.String(80), db.ForeignKey(DOCENTE_TABLE_NAME+'.matr_d'), nullable=False)
  
class Esame(db.Model):
    __tablename__ = ESAME_TABLE_NAME
    cod_e = db.Column(db.Integer, primary_key=True)
    cod_c = db.Column(db.String(80), db.ForeignKey(CORSO_TABLE_NAME+'.cod_c'), nullable=False)
    matr_s = db.Column(db.String(80), db.ForeignKey(STUDENTE_TABLE_NAME+'.matr_s'), nullable=False)
    data= db.Column(db.Date, nullable=False)
    voto = db.Column(db.Integer, nullable=False)    

def init_db(app):
    
    db.create_all()
    
    # Se la tabella non è popolata
        #   Se il file esiste
            # Leggere e caricare i dati
        # Se no, Fermarsi
    # Se lo è, fermarsi 
    
    if not Studente.query.first():
        if os.path.exists(STUDENTE_TABLE_CSV):
            with open(STUDENTE_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    new_record = Studente(
                       matr_s=row["MatrS"],
                       nome_s = row["NomeS"],
                       citta = row["Città"],
                    )
                    db.session.add(new_record)
                #modifiche si propagano sul db
                db.session.commit()
                app.logger.info(f"Tabella {STUDENTE_TABLE_NAME} è stata popolata")    
        else:
            app.logger.info(f"File {STUDENTE_TABLE_CSV} non esiste")
            sys.exit(1)    
    else:
        app.logger.info(f"Tabella {STUDENTE_TABLE_NAME} già popolata.")


    if not Docente.query.first():
        if os.path.exists(DOCENTE_TABLE_CSV):
            with open(DOCENTE_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    new_record = Docente(
                       matr_d=row["MatrD"],
                       nome_d = row["NomeD"]
                    )
                    db.session.add(new_record)
                #modifiche si propagano sul db
                db.session.commit()
                app.logger.info(f"Tabella {DOCENTE_TABLE_NAME} è stata popolata")    
        else:
            app.logger.info(f"File {DOCENTE_TABLE_CSV} non esiste")
            sys.exit(1)    
    else:
        app.logger.info(f"Tabella {DOCENTE_TABLE_NAME} già popolata.")
     
    if not Corso.query.first():
        if os.path.exists(CORSO_TABLE_CSV):
            with open(CORSO_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    new_record = Corso(
                       matr_d=row["MatrD"],
                       cod_c = row["NomeC"],
                       nome_c = row["NomeC"]
                    )
                    db.session.add(new_record)
                #modifiche si propagano sul db
                db.session.commit()
                app.logger.info(f"Tabella {CORSO_TABLE_NAME} è stata popolata")    
        else:
            app.logger.info(f"File {CORSO_TABLE_CSV} non esiste")
            sys.exit(1)    
    else:
        app.logger.info(f"Tabella {CORSO_TABLE_NAME} già popolata.")
                                                            
    if not Esame.query.first():
        if os.path.exists(ESAME_TABLE_CSV):
            with open(ESAME_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    new_record = Esame(
                       matr_s=row["MatrS"],
                       cod_c = row["CodC"],
                       voto = row["Voto"],
                       data = datetime.strptime(row["Data"], "%Y-%m-%d")
                    )
                    db.session.add(new_record)
                #modifiche si propagano sul db
                db.session.commit()
                app.logger.info(f"Tabella {ESAME_TABLE_NAME} è stata popolata")    
        else:
            app.logger.info(f"File {ESAME_TABLE_CSV} non esiste")
            sys.exit(1)    
    else:
        app.logger.info(f"Tabella {ESAME_TABLE_NAME} già popolata.")
                                                            