import locale
from flask import Flask, flash, render_template, jsonify, request, session, redirect, url_for
from models import db, init_db, Lotto, Prodotto, Produttore, User, Prenotazione
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

# Mostra l'elenco dei lotti disponibili
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/prenotazioni')
def mostra_prenotazioni():
    return render_template('prenotazioni.html')


# Restituisce i dati dei lotti disponibili in formato JSON
@app.route('/api/lotti', methods=['GET'])
def get_lotti():

    # Leggo i parametri passati in query string
    order = request.args.get('order', 'asc')

    if order == 'asc':
        lotti = Lotto.query.order_by(Lotto.data_consegna).all()  # -> list es. [<Lotto 1>, <Lotto 2>, ...]
    elif order == 'desc':
        lotti = Lotto.query.order_by(Lotto.data_consegna.desc()).all()
    else:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'

    lotti_data = []
    for lotto in lotti:
        dict_lotto = lotto.to_dict()
        lotti_data.append(dict_lotto)

    return jsonify(lotti_data)


@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    
    prenotazioni = Prenotazione.query \
        .filter_by(user_id=session['user_id']) \
        .join(Lotto, Lotto.id == Prenotazione.lotto_id) \
        .order_by(Lotto.data_consegna) \
        .all()  # -> list es. [<Prenotazione 1>, <Prenotazione 2>, ...]

    prenot_data = []
    for prenot in prenotazioni:
        dict_prenot = prenot.to_dict()
        prenot_data.append(dict_prenot)

    return jsonify(prenot_data)


# Mostra il form per la nuova prenotazione di un lotto (GET)
@app.route('/lotto/<int:id_lotto>', methods=['GET'])
def mostra_lotto(id_lotto):
    # Controllare che l'utente sia loggato
    if 'user_id' not in session:
        return redirect(url_for('login'))


    # Ottengo il record del lotto a partire dal suo ID
    lotto = db.session.get(Lotto, id_lotto)
    if not lotto:
        return 'Lotto non trovato!', 404

    # user = db.session.get(User, session['user_id'])
    # prenotazioni = user.rel_prenotazioni

    prenot_utente = Prenotazione.query.filter_by(
        user_id=session['user_id'],
        lotto_id=id_lotto
    ).first()

    # Se l'utente ha delle prenotazioni su qusto specifico lotto
    if prenot_utente:
        return redirect(url_for('mostra_prenotazione', prenotazione_id=prenot_utente.id))
    # Se l'utente non ha delle prenotazioni su qusto specifico lotto
    else:
        return render_template('lotto.html', lotto=lotto)


# Riceve i dati del form per la nuova prenotazione di un lotto (POST)
@app.route('/lotto/<int:id_lotto>', methods=['POST'])
def nuova_prenotazione(id_lotto):
    # Controllare che l'utente sia loggato
    if 'user_id' not in session:
        return 'Non sei autorizzato', 401

    quantita = int(request.form.get('quantita'))

    # Controllo che sia una quantità >= 1
    if quantita < 1:
        # @TODO: fix flask messages
        flash('La quantità deve essere mggiore di zero!', 'warning')
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))
    

    # Controllo che la quantità sia minore o uguale alla qta disponibile
    lotto = db.session.get(Lotto, id_lotto)
    if quantita > lotto.get_qta_disponibile():
        flash('Hai prenotato di più della quantità disponibile.', 'warning')
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))

    new_prenotazione = Prenotazione(qta=quantita, lotto_id=id_lotto, user_id=session['user_id'])
    db.session.add(new_prenotazione)
    db.session.commit()
    flash('Prenotazione effettuata con successo!', 'success')

    return redirect(url_for('mostra_prenotazioni'))

    

# Mostra il form per la modifica di una prenotazione esistente (GET)
@app.route('/prenotazione/<int:prenotazione_id>', methods=['GET'])
def mostra_prenotazione(prenotazione_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        pass

    prenotazione = db.session.get(Prenotazione, prenotazione_id)

    if not prenotazione:
        flash('Prenotazione non trovata.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

    if prenotazione.user_id != session['user_id']:
        flash('Non sei autorizzato a visualizzare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))

    return render_template('prenotazione.html', prenotazione=prenotazione)


# Riceve i dati del form per la modifica di una prenotazione esistente (POST)
@app.route('/prenotazione/<int:prenotazione_id>', methods=['POST'])
def modifica_prenotazione(prenotazione_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    prenotazione = db.session.get(Prenotazione, prenotazione_id)

    if not prenotazione:
        flash('Prenotazione non trovata.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

    if prenotazione.user_id != session['user_id']:
        flash('Non sei autorizzato a modificare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))
    else:
        pass

    azione = request.form.get('azione')

    if azione == 'aggiorna':
        quantita = int(request.form.get('quantita'))  # ATTENZIONE: sarebbe da gestire meglio
                                                      # con un try/except per evitare errori
        lotto = prenotazione.rel_lotto

        if quantita <= 0:
            flash('Quantità non valida. Inserire un numero maggiore di 0.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_id))

        qta_disponibile = lotto.get_qta_disponibile()

        if quantita > qta_disponibile + prenotazione.qta:
            flash('La quantità richiesta supera quella disponibile.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=prenotazione_id))

        prenotazione.qta = quantita
        db.session.commit()
        flash(f'Prenotazione di "{lotto.rel_prodotto.nome_prodotto}" aggiornata a {quantita} {lotto.qta_unita_misura}.', 'success')

    elif azione == 'elimina':
        db.session.delete(prenotazione)
        db.session.commit()
        flash('Prenotazione eliminata con successo.', 'warning')

    else:
        flash('Azione non implementata.', 'danger')

    return redirect(url_for('mostra_prenotazioni'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # ATTENZIONE: Possiamo usare la password come parametro di ricerca
        #             perché l'abbiamo memorizzata in chiaro (e non come "hash")
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            # flash('Login riuscito!')
            return redirect(url_for('home'))
        else:
            # flash('Credenziali non valide!')
            return redirect(url_for('login'))
    
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    # flash('Logout effettuato con successo!')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)