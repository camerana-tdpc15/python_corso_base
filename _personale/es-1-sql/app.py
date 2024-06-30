# 1 importo Flask
from flask import Flask, jsonify

from setting import DATABASE

from models import db, init_db, Concerto, Sala, Orchestra


# 2 Creo applicazione di Flask
app = Flask(__name__)


# 3. configuro le impostazioni di flask attraverso la funzione 'app.config.update'
app.config.update(
    # Questa è la stringa di connessione al database IMPORTANTE!!!
    SQLALCHEMY_DATABSE_URL='sqlite:///' + DATABASE,
    DEBUG=True
)

# 4 inizializzo il db tramite la funzione 'db.init_app()'
db.Init_app(app)




# 6 faccio le query che ci chiede l'esercizio:
# Trovare il codice e il nome dell'orchestra con più di 30 elementi
# che hanno tenuto concerti sia a Torino, che Milano, 
# e non hanno mai tenuto concerti a Bologna 

# per comodita facciamo più query e le colleghiamo tra di loro

# 6.1 Creo una Route 
@app.route('/')
def query():
    # 6.2 creo una subquery per fare JOIN per OTTENERE TUTTI I CONCERTI LA CUI SALA è A TORINO
    subquery_torino = db.session.query(Concerto.Cod_O).join(Sala).filter(   # uso db.session perchè è più comodo
        Sala.Citta == 'Torino'                                             # la query la deve fare sul codice dell'orchestra ' Concerto.CodO'
        ).subquery()                                                       # con 'join' vado a fare il merge con 'Sala'
                                                                           # faccio il where con 'filter' dove la città è = a 'Torino'
                                                                           # con 'subquery()' indico che quella è una sunquery!
                                                                           

    # 6.3 creo una subquery per fare JOIN per OTTENERE TUTTI I CONCERTI LA CUI SALA è A MILANO
    subquery_milano = db.session.query(Concerto.Cod_O).join(Sala).filter(   # uso db.session perchè è più comodo
        Sala.Citta == 'Milano'                                             # la query la deve fare sul codice dell'orchestra ' Concerto.CodO'
        ).subquery()                                                       # con 'join' vado a fare il merge con 'Sala'
                                                                           # faccio il where con 'filter' dove la città è = a 'Milano'
                                                                           # con 'subquery()' indico che quella è una sunquery!
                                                                           
                                                                           
    # 6.4 creo una subquery per fare JOIN per OTTENERE TUTTI I CONCERTI LA CUI SALA è A BOLOGNA
    subquery_bologna = db.session.query(Concerto.Cod_O).join(Sala).filter(   # uso db.session perchè è più comodo
        Sala.Citta == 'Bologna'                                             # la query la deve fare sul codice dell'orchestra ' Concerto.CodO'
        ).subquery()                                                       # con 'join' vado a fare il merge con 'Sala'
                                                                           # faccio il where con 'filter' dove la città è = a 'Torino'
                                                                           # con 'subquery()' indico che quella è una sunquery!
                                                                           
                                                              
    # 7 una volta che ho tutte le subquery faccio la query principale
    result = db.session.query(Orchestra.cod_o, Orchestra.name_o).filter(
        Orchestra.num_elementi > 30,
        Orchestra.cod_o.in_(subquery_torino), # le orchestre che hanno fatto concerti a Torino
        Orchestra.cod_o.in_(subquery_milano),  # le orchestre che hanno fatto concerti a Milano
        Orchestra.cod_o.notin_(subquery_bologna),  # le orchestre che non si trovano tra quelle che hanno fatto concerti a Bologna
    ).all()   # con 'all()' chiedo di mostrarmi tutte le righe che rispettano questa query
    
    return jsonify([{'CodO': r[0, 'NomeO' : r[1]]}for r in result])  # vado a mostrare i risultati che ottengo dalla query
                                                                    # usando questa funzione per trasformare il result che è un dizionario in Json cioè una stringa                                          
                                                                 
                                                                 




# 5 faccio fare il 'run
if __name__ == '__main__':
    # andando a definire il contesto dell'app cioè fa runnare il db
    with app.app_context():
        init_db(app)
    # faccio runnare l'applicaione Flask
    app.run()

