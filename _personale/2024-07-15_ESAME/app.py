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
    return render_template('index.html')

@app.route('/prenotazioni')
def mostra_prenotazioni():
    return render_template('prenotazioni.html')


# Restituisce i dati dei lotti disponibili in formato JSON
@app.route('/api/eventi', methods=['GET'])
def get_lotti():

    # Leggo i parametri passati in query string
    order = request.args.get('order', 'asc')

    if order == 'asc':
        eventi = Evento.query.order_by(Evento.nome_evento).all()  # -> list es. [<Lotto 1>, <Lotto 2>, ...]
    elif order == 'desc':
        eventi = Evento.query.order_by(Evento.nome_evento.desc()).all()
    else:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'

    eventi_data = []
    for evento in eventi:
        dict_lotto = lotto.to_dict()
        lotti_data.append(dict_lotto)

    return jsonify(lotti_data)




if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)