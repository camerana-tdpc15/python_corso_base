# PRIMA FAI SETTING!!!

# 1. importo la cartella
import csv
from datetime import datetime
import os
import sys
from flask_sqlalchemy import SQLAlchemy


# 4. importo tramite 'setting' i nomi delle tabelle e i percorsi
from setting import CONCERTO_TABLE_NAME, ORCHESTRA_TABLE_NAME, SALA_TABLE_NAME,SALA_TABLE_CSV, ORCHESTRA_TABLE_CSV, CONCERTI_TABLE_CSV


# 2. inizializzo un'istanza di database
db = SQLAlchemy()


# 3. vado a creare le varie tabelle sull'istanza di database appena creato
class Concerto (db.Model):
    
    # 5.1 creo le varie strutture della tabella Concerto
    __tablename__ = CONCERTO_TABLE_NAME
    cod_c = db.Column(db.Integer, primary_key = True)
    data = db.Cplomn(db.Date, nullable = False)
    cod_o = db.Column(db.Integer, db.models.ForeignKey(ORCHESTRA_TABLE_NAME+ 'cod_o'), nullable = False) # qui definisco le chiavi esterne,uso 'ForeignKey' per dirgli che quella chiave
                                                                             # la devi andare a prendere dalla tabella Orchestra + il cod_o
    cod_s = db.Column(db.Integer, db.models.ForeignKey(SALA_TABLE_NAME+ 'cod_s'), nullable = False)
    prezzo_biglietto = db.Column(db.Float, nullable = False)
                                                                   
class Orchestra (db.Model):
    __tablename__ = ORCHESTRA_TABLE_NAME
    # 5.2 creo le varie strutture della tabella Orchestra
    cod_o = db.Column(db.Integer, primary_key = True)
    name_o = db.Column(db.String(80), nullable = False )
    name_direttore = db.Column(db.String(80))
    num_elementi = db.Column(db.String(80))
    
class Sala (db.Model):
    __tablename__ = SALA_TABLE_NAME
    # 5.3 creo le varie strutture della tabella Sala
    cod_s = db.Column(db.Integer, primary_key = True)
    name_s = db.Column(db.String(80), nullable = False ) # NULLABLE = FALSE VUOL DIRE CHE E' OBBLIGATORIO!!
    Citta = db.Column(db.String(80), nullable = False)
    capienza = db.Column(db.Integer, nullable = False)
    



# 6 faccio la funzione che ci permette di prendere tutti i dati dal csv e importarli all'interno delle varie tabelle
# 6.1 questa è una funzione che inizializza il  db alla quale passiamo l'applicazione di flask che ci permette di fare dei logger
def init_db(app):    
    
    # 6.2 diciamo al db di creare tutte le tabelle
    db.create_all()    
    
    # 6.3 devo fare una query per vedere se c'è qualcosa nella tabella SALA verificando
    # se la tabella NON e' popolata
    if not Sala.query.first(): # se NON esiste il primo elemento della Sala
        # 6.3.1 Verifico se il file ESISTE
        
        if os.path.exists(SALA_TABLE_CSV): # se esiste il percorso specifico del file csv
            # 6.3.1.1 deve leggere ecaricare i dati
            
            with open(SALA_TABLE_CSV, 'r') as csv_file: # apri e leggo il file, quando faccio 'whit' 
                                                       # devo specificare il nome di come lo posso chiamare quindi scrivo 'as csv_file'
                                                       
                # 6.3.1.2 trasformo questo file in un ARRAY DI DICT
                csv_reader = csv.DictReader(csv_file)
                
                # 6.3.1.3 avendo ora un'array faccio un ciclo for per ogni riga dell'array..
                for row in csv_file:
                    # 6.3.1.4 aggiungo 1 nuovo record di tipo Sala
                    new_record = Sala(
                        # 6.3.1.5 prendiamo i dati e li andiamo a mettere nelnuovo record di tipo Sala
                        cod_s = row['CodS'],
                        nome_s = row['NomeS'],
                        citta = row['Citta'],
                        capienza = row['Capienza']                        
                    )
                    # 6.3.1.6 ora devo aggiungere il nuovo record
                    db.session.add(new_record)
                    
                    # 6.3.1.7 ora devo salvare il nuovo record
                    db.session.commit()
                    
                    # 6.3.1.8 comunico che il record è stato importato correttamente
                    app.logger.info(f'Tabella {SALA_TABLE_NAME} è stata popolata')
                    
        else:
            # 6.3.2 Oppure se NON esiste si deve fermare
            app.logger.info(f"File {SALA_TABLE_CSV} non esiste")
            
             # 6.3.3 in questo caso gli dico di BLOCCARE IL SITEMA perchè se non ci sono i dati non puoi fare nulla
            sys.exit(1)
            
    else:
        # 6.4 oppure se E' popolatta si deve fermare
        app.logger.info(f"Tabella {SALA_TABLE_NAME} è già popolata") # uso il logger di Flask per dirgli..
        
        
    # 6.3 devo fare una query per vedere se c'è qualcosa nella tabella ORCHESTRA verificando
    # se la tabella NON e' popolata
    if not Orchestra.query.first(): # se NON esiste il primo elemento della Sala
        # 6.3.1 Verifico se il file ESISTE
        
        if os.path.exists(ORCHESTRA_TABLE_CSV): # se esiste il percorso specifico del file csv
            # 6.3.1.1 deve leggere ecaricare i dati
            
            with open(ORCHESTRA_TABLE_CSV, 'r') as csv_file: # apri e leggo il file, quando faccio 'whit' 
                                                       # devo specificare il nome di come lo posso chiamare quindi scrivo 'as csv_file'
                                                       
                # 6.3.1.2 trasformo questo file in un ARRAY DI DICT
                csv_reader = csv.DictReader(csv_file)
                
                # 6.3.1.3 avendo ora un'array faccio un ciclo for per ogni riga dell'array..
                for row in csv_file:
                    # 6.3.1.4 aggiungo 1 nuovo record di tipo Sala
                    new_record = Orchestra(
                        # 6.3.1.5 prendiamo i dati e li andiamo a mettere nelnuovo record di tipo Sala
                        cod_o = row['CodO'],
                        nome_o = row['NomeO'],
                        nome_direttore = row['NomeDirettore'],
                        num_elementi = row['NumElementi']                        
                    )
                    # 6.3.1.6 ora devo aggiungere il nuovo record
                    db.session.add(new_record)
                    
                    # 6.3.1.7 ora devo salvare il nuovo record
                    db.session.commit()
                    
                    # 6.3.1.8 comunico che il record è stato importato correttamente
                    app.logger.info(f'Tabella {ORCHESTRA_TABLE_NAME} è stata popolata')
                    
        else:
            # 6.3.2 Oppure se NON esiste si deve fermare
            app.logger.info(f"File {ORCHESTRA_TABLE_CSV} non esiste")
            
             # 6.3.3 in questo caso gli dico di BLOCCARE IL SITEMA perchè se non ci sono i dati non puoi fare nulla
            sys.exit(1)
            
    else:
        # 6.4 oppure se E' popolatta si deve fermare
        app.logger.info(f"Tabella {ORCHESTRA_TABLE_NAME} è già popolata") # uso il logger di Flask per dirgli..
        
        
    # 6.3 devo fare una query per vedere se c'è qualcosa nella tabella CONCERTI verificando
    # se la tabella NON e' popolata
    if not Concerto.query.first(): # se NON esiste il primo elemento della Sala
        # 6.3.1 Verifico se il file ESISTE
        
        if os.path.exists(CONCERTI_TABLE_CSV): # se esiste il percorso specifico del file csv
            # 6.3.1.1 deve leggere ecaricare i dati
            
            with open(CONCERTI_TABLE_CSV, 'r') as csv_file: # apri e leggo il file, quando faccio 'whit' 
                                                       # devo specificare il nome di come lo posso chiamare quindi scrivo 'as csv_file'
                                                       
                # 6.3.1.2 trasformo questo file in un ARRAY DI DICT
                csv_reader = csv.DictReader(csv_file)
                
                # 6.3.1.3 avendo ora un'array faccio un ciclo for per ogni riga dell'array..
                for row in csv_file:
                    # 6.3.1.4 aggiungo 1 nuovo record di tipo Sala
                    new_record = Concerto(
                        # 6.3.1.5 prendiamo i dati e li andiamo a mettere nelnuovo record di tipo Sala
                        cod_c = row['CodC'],
                        data = datetime.strptime(row['Data']), # la funzione 'datetime.strptime' ci permette di formattare una stringa in una data 
                                                               # con la formattazione richiesta
                        cod_s = row['CodS'],
                        prezzo_biglietto = row['PrezzoBiglietto']                
                    )
                    # 6.3.1.6 ora devo aggiungere il nuovo record
                    db.session.add(new_record)
                    
                    # 6.3.1.7 ora devo salvare il nuovo record
                    db.session.commit()
                    
                    # 6.3.1.8 comunico che il record è stato importato correttamente
                    app.logger.info(f'Tabella {CONCERTO_TABLE_NAME} è stata popolata')
                    
        else:
            # 6.3.2 Oppure se NON esiste si deve fermare
            app.logger.info(f"File {CONCERTI_TABLE_CSV} non esiste")
            
             # 6.3.3 in questo caso gli dico di BLOCCARE IL SITEMA perchè se non ci sono i dati non puoi fare nulla
            sys.exit(1)
            
    else:
        # 6.4 oppure se E' popolatta si deve fermare
        app.logger.info(f"Tabella {CONCERTO_TABLE_NAME} è già popolata") # uso il logger di Flask per dirgli..
        
# 7 VADO SUL FILE APP.PY!!!!