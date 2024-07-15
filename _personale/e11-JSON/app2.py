import locale
from flask import Flask, render_template, jsonify, request, session, flash, redirect, url_for
from models import db, init_db, Lotto, Prodotto, Produttore, User, Prenotazione
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)

# Mostra l'elenco dei lotti disponibili
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prenotazioni')
def mostra_prenotazioni():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('prenotazioni.html')

# Restituisce i dati dei lotti disponibili in formato JSON
@app.route('/api/lotti', methods=['GET'])
def get_lotti():
    order = request.args.get('order', 'asc')
    if order == 'asc':
        lotti = Lotto.query.order_by(Lotto.data_consegna).all()
    elif order == 'desc':
        lotti = Lotto.query.order_by(Lotto.data_consegna.desc()).all()
    else:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'

    lotti_data = [lotto.to_dict() for lotto in lotti]
    return jsonify(lotti_data)

@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    prenotazioni = Prenotazione.query \
        .filter_by(user_id=session['user_id']) \
        .join(Lotto, Lotto.id == Prenotazione.lotto_id) \
        .order_by(Lotto.data_consegna) \
        .all()

    prenot_data = [prenot.to_dict() for prenot in prenotazioni]
    return jsonify(prenot_data)

@app.route('/lotto/<int:id_lotto>', methods=['GET'])
def mostra_lotto(id_lotto):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    lotto = db.session.get(Lotto, id_lotto)
    if not lotto:
        return 'Lotto non trovato!', 404

    prenot_utente = Prenotazione.query.filter_by(
        user_id=session['user_id'],
        lotto_id=id_lotto
    ).first()

    if prenot_utente:
        return redirect(url_for('mostra_prenotazione', prenotazione_id=prenot_utente.id))
    return render_template('lotto.html', lotto=lotto)

@app.route('/lotto/<int:id_lotto>', methods=['POST'])
def nuova_prenotazione(id_lotto):
    if 'user_id' not in session:
        flash('Non sei autorizzato, per favore fare login', 'warning')
        return redirect(url_for('login'))

    try:
        quantita = int(request.form.get('quantita'))
    except ValueError:
        flash('Quantità non valida. Inserire un numero valido.', 'danger')
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))

    if quantita < 1:
        flash('La quantita deve essere maggiore di zero!', 'warning')
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))

    lotto = db.session.get(Lotto, id_lotto)
    if quantita > lotto.get_qta_disponibile():
        flash('Hai prenotato di più della quantità disponibile.', 'warning')
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))

    new_prenotazione = Prenotazione(qta=quantita, lotto_id=id_lotto, user_id=session['user_id'])
    db.session.add(new_prenotazione)
    db.session.commit()
    flash('Prenotazione effettuata con successo!', 'success')
    return redirect(url_for('prenotazioni'))

@app.route('/prenotazione/<int:prenotazione_id>', methods=['GET'])
def mostra_prenotazione(prenotazione_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    prenotazione = db.session.get(Prenotazione, prenotazione_id)
    if not prenotazione:
        flash('Prenotazione non trovata.', 'danger')
        return redirect(url_for('prenotazioni'))

    if prenotazione.user_id != session['user_id']:
        flash('Non sei autorizzato a visualizzare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))

    return render_template('prenotazione.html', prenotazione=prenotazione)

@app.route('/prenotazione/<int:id_prenotazione>', methods=['POST'])
def modifica_prenotazione(id_prenotazione):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    prenotazione = db.session.get(Prenotazione, id_prenotazione)
    if not prenotazione:
        flash('Prenotazione non trovata', 'danger')
        return redirect(url_for('prenotazioni'))

    if prenotazione.user_id != session['user_id']:
        flash('Non sei autorizzato a modificare questa prenotazione.', 'danger')
        return redirect(url_for('prenotazioni'))

    azione = request.form.get('azione')
    if azione == 'aggiorna':
        try:
            quantita = int(request.form.get('quantita'))
        except ValueError:
            flash('Quantità non valida. Inserire un numero valido.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=id_prenotazione))

        if quantita <= 0:
            flash('Quantità non valida. Inserire un numero maggiore di 0.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=id_prenotazione))

        lotto = prenotazione.lotto
        qta_disponibile = lotto.get_qta_disponibile()
        if quantita > qta_disponibile + prenotazione.qta:
            flash('La quantità richiesta supera quella disponibile.', 'danger')
            return redirect(url_for('mostra_prenotazione', prenotazione_id=id_prenotazione))

        prenotazione.qta = quantita
        db.session.commit()
        flash(f'Prenotazione di "{lotto.prodotto.nome}" aggiornata a {quantita} {lotto.qta_unita_misura}.', 'success')

    elif azione == 'elimina':
        db.session.delete(prenotazione)
        db.session.commit()
        flash('Prenotazione eliminata con successo', 'warning')

    else:
        flash('Azione non implementata', 'danger')

    return redirect(url_for('prenotazioni'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash(f'Login riuscito. Benvenuto {user.nome}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenziali non valide!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
