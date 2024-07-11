import locale
from flask import Flask, render_template, jsonify, request
from models import db, init_db, Lotto, Prodotto, Produttore, User
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/produttori')
def produttori():
    return render_template('produttori.html')


@app.route('/utenti')
def utenti():
    return render_template('utenti.html')


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


@app.route('/api/produttori', methods=['GET'])
def get_prod():

    # Leggo i parametri passati in query string
    order = request.args.get('order', 'asc')

    if order == 'asc':
        produttore = Produttore.query.order_by(Produttore.nome_produttore).all()
    elif order == 'desc':
        produttore = Produttore.query.order_by(Produttore.nome_produttore.desc()).all()
    else:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'

    prod_data = []
    for prod in produttore:
        dict_prod = prod.to_dict()
        prod_data.append(dict_prod)

    return jsonify(prod_data)


@app.route('/api/utenti', methods=['GET'])
def get_utenti():

    # Leggo i parametri passati in query string
    order = request.args.get('order', 'asc')

    if order == 'asc':
        utente = User.query.order_by(User.nome).all()
    elif order == 'desc':
        utente = User.query.order_by(User.nome.desc()).all()
    else:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'

    user_data = []
    for user in utente:
        dict_user = user.to_dict()
        user_data.append(dict_user)

    return jsonify(user_data)


@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    ...


# @TODO: Implementare il login / logout
...

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)