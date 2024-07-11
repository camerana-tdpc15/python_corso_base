import locale
from flask import Flask, render_template, jsonify, request,session, redirect  
from models import db, init_db, Lotto, Prodotto, Produttore , User, Prenotazione
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

@app.route('/')
def home():
    return render_template('home.html')



@app.route('/api/lotti', methods=['GET'])
def get_lotti():

    # Leggo i parametri passati in query string
    order = request.args.get('order', 'asc')

    if order == 'asc':
        lotti = Lotto.query.order_by(Lotto.data_consegna).all()
    elif order == 'desc':
        lotti = Lotto.query.order_by(Lotto.data_consegna.desc()).all()
    else:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'

    lotti_data = []
    for lotto in lotti:
        dict_lotto = lotto.to_dict()
        lotti_data.append(dict_lotto)

    return jsonify(lotti_data)

@app.route('/lotto/<id_lotto>')
def mostra_lotto(id_lotto):
    #  controllare che l'utente sia loggato
    if 'user_id' in session:
        return redirect(url_for('login'))

    # Ottengo il record del lotto a partire dal suo ID
    lotto = db.session.get(lotto, id_lotto)
    if not lotto:
        return 'lotto non trovato!', 404
    user = db.session.get(User, session['user_id'])
    # prenotazioni = user.real_prenotazioni

    prenot_utente = Prenotazione. query.filter_by(
        user_id=session['user_id']
        lotto_id=id_lotto
    )
    
    # se l'utente ha delle prenotazioni
    if prenot_utente:
        return render_template('modifica_prenotazione.html')
    # se l'utente non ha delle prenotazioni
    else:
        return render_template('nuova_prenotazione.html')
    
    @app.route('/prenotazione/<int:id_prenorazione>', methods=['GET'])
    DEF aggiorna_prenotazioni(id_prenotazione),

@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    ...


# @TODO: Implementare il login / logout
...

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)