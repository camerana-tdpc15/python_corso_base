import locale
from flask import Flask, flash, render_template, jsonify, request, session, redirect, url_for
from models import db, init_db, Evento, Locale, Prenotazione, Replica, Utente
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'


db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask


# Mostra l'elenco dei lotti disponibili
@app.route('/')
def home():
    return 'prova database'
    #return render_template('home.html')




if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)