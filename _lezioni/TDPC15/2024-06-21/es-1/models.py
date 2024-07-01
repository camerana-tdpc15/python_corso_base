import csv
from datetime import datetime
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from settings import CONCERTO_TABLE_NAME,ORCHESTRA_TABLE_NAME,SALE_TABLE_NAME, SALA_TABLE_CSV, ORCHESTRA_TABLE_CSV, CONCERTO_TABLE_CSV

db  = SQLAlchemy()

class Concerto(db.Model):
    __tablename__ = CONCERTO_TABLE_NAME
    cod_c = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    cod_o = db.Column(db.Integer, db.ForeignKey(ORCHESTRA_TABLE_NAME+'.cod_o'), nullable=False)
    cod_s = db.Column(db.Integer, db.ForeignKey(SALE_TABLE_NAME+'.cod_s'), nullable=False)
    prezzo_biglietto = db.Column(db.Float, nullable=False)
    

class Orchestra(db.Model):
    __tablename__ = ORCHESTRA_TABLE_NAME
    cod_o = db.Column(db.Integer, primary_key=True)
    nome_o = db.Column(db.String(80), nullable=False)
    nome_direttore = db.Column(db.String(80))
    num_elementi = db.Column(db.String(80))    

class Sala(db.Model):
    __tablename__ = SALE_TABLE_NAME
    cod_s = db.Column(db.Integer, primary_key=True)
    nome_s = db.Column(db.String(80), nullable=False)
    citta = db.Column(db.String(80), nullable=False)
    capienza = db.Column(db.Integer, nullable=False)
    

def init_db(app):
    
    db.create_all()
    
    # Se la tabella non è popolata
        #   Se il file esiste
            # Leggere e caricare i dati
        # Se no, Fermarsi
    # Se lo è, fermarsi 
    
    if not Sala.query.first():
        if os.path.exists(SALA_TABLE_CSV):
            with open(SALA_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    new_record = Sala(
                       cod_s=row["CodS"],
                       nome_s = row["NomeS"],
                       citta = row["Città"],
                       capienza = row["Capienza"] 
                    )
                    db.session.add(new_record)
                #modifiche si propagano sul db
                db.session.commit()
                app.logger.info(f"Tabella {SALE_TABLE_NAME} è stata popolata")    
        else:
            app.logger.info(f"File {SALA_TABLE_CSV} non esiste")
            sys.exit(1)    
    else:
        app.logger.info(f"Tabella {SALE_TABLE_NAME} già popolata.")
        
    if not Orchestra.query.first():
        if os.path.exists(ORCHESTRA_TABLE_CSV):
            with open(ORCHESTRA_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    new_record = Orchestra(
                       cod_o=row["CodO"],
                       nome_o = row["NomeO"],
                       nome_direttore = row["NomeDirettore"],
                       num_elementi = row["NumElementi"] 
                    )
                    db.session.add(new_record)
                #modifiche si propagano sul db
                db.session.commit()
                app.logger.info(f"Tabella {ORCHESTRA_TABLE_NAME} è stata popolata")    
        else:
            app.logger.info(f"File {ORCHESTRA_TABLE_CSV} non esiste")
            sys.exit(1)    
    else:
        app.logger.info(f"Tabella {ORCHESTRA_TABLE_NAME} già popolata.")        
        

    if not Concerto.query.first():
        if os.path.exists(CONCERTO_TABLE_CSV):
            with open(CONCERTO_TABLE_CSV, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                
                for row in csv_reader:
                    new_record = Concerto(
                       cod_c=row["CodC"],
                       data=datetime.strptime(row["Data"], "%Y-%m-%d"),
                       cod_s=row["CodS"],
                       cod_o=row["CodO"],
                       prezzo_biglietto = row["PrezzoBiglietto"]
                    )
                    db.session.add(new_record)
                #modifiche si propagano sul db
                db.session.commit()
                app.logger.info(f"Tabella {CONCERTO_TABLE_NAME} è stata popolata")    
        else:
            app.logger.info(f"File {CONCERTO_TABLE_CSV} non esiste")
            sys.exit(1)    
    else:
        app.logger.info(f"Tabella {CONCERTO_TABLE_NAME} già popolata.")                