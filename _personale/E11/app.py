from flask import Flask, request, render_template, redirect, url_for, session, flash
from settings import DATABASE
from models import init_db, db, users, lotti,prenotazioni,prodotti,produttori

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE,  # Il path al database
    DEBUG=True  # Imposto qua la modalità debug
                # Vedi app.run() alla fine del file
)

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask


@app.route('/')
def home():
    
    return render_template('home.html')






if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run()  # Notate che ho rimosso il parametro `debug=True` perché ora è
               # impostato in `app.config`. Questo perché altriment la funzione
               # init_db si ritroverebbe il livello di logging non impostato (0).