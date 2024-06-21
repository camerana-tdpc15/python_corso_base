#  Importa la classe Flask dal modulo Flask. 
from flask import Flask
from settings import DATABASE
from models import db
# Crea un'istanza di Flask con il nome dell'applicazione. 
app = Flask(__name__)

#  Aggiorna la configurazione dell'applicazione con le seguenti impostazioni: 
app.config.update(
    
    #  Una chiave segreta utilizzata per proteggere i dati sensibili. 
    SECRET_KEY='my_very_secret_key123',

    # Il percorso al database SQLite. 
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE,  # Il path al database
    
    #  Imposta la modalità di debug su True. 
    DEBUG=True  # Imposto qua la modalità debug
                # Vedi app.run() alla fine del file
)

# Inizializza l'istanza di SQLAlchemy con l'app Flask per interagire con il database. 
db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

# Controlla se lo script è eseguito direttamente come programma principale. 
if __name__ == '__main__':
    # Crea un contesto dell'applicazione per eseguire le operazioni all'interno. 
    with app.app_context():
        #  Chiama la funzione  init_db  per inizializzare il database. 
        init_db(app)

    # Avvia il server web integrato per eseguire l'applicazione Flask. 
    app.run()  # Notate che ho rimosso il parametro `debug=True` perché ora è
               # impostato in `app.config`. Questo perché altriment la funzione
               # init_db si ritroverebbe il livello di logging non impostato (0).
