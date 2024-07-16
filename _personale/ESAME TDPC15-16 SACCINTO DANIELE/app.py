import locale as loc
from flask import Flask, flash, render_template, jsonify, request, session, redirect, url_for
from models import db, init_db, Prenotazione, Utente, Replica, Evento, Locale
from settings import DATABASE_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)

@app.route('/')
def iniziale():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/prenotazioni', methods=['GET'])
def pag_prenot():
    if 'utente_id' not in session:
        return redirect(url_for('login'))

    prenotazioni_ = Prenotazione.query \
        .filter_by(utente_id=session['utente_id']) \
        .join(Replica, Replica.id == Prenotazione.replica_id) \
        .order_by(Replica.data_ora) \
        .all()

    return render_template('Prenotazioni.html', prenotazioni=prenotazioni_)

@app.route('/eventi')
def pag_eventi():
    eventi = Evento.query.all()
    repliche = Replica.query.all()
    return render_template('eventi.html', eventi=eventi, repliche=repliche)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Utente.query.filter_by(email=email, password=password).one_or_none()
        if user:
            session['utente_id'] = user.id
            flash('Login riuscito!')
            return redirect(url_for('home'))
        else:
            flash('Credenziali non valide!')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('utente_id', None)
    print(session)  # Controllo il contenuto della sessione
    flash('Logout effettuato con successo!')
    return redirect(url_for('login'))


@app.route('/api/eventi', methods=['GET'])
def get_eventi():
    order = request.args.get('order', 'asc')
    if order not in ['asc', 'desc']:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".', 400

    order_by = Replica.data_ora.asc() if order == 'asc' else Replica.data_ora.desc()
    repliche = Replica.query.order_by(order_by).all()

    return jsonify([r.to_dict() for r in repliche])

@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    if 'utente_id' not in session:
        return redirect(url_for('login'))

    prenotazioni_ = Prenotazione.query \
        .filter_by(utente_id=session['utente_id']) \
        .join(Replica, Replica.id == Prenotazione.replica_id) \
        .order_by(Replica.data_ora) \
        .all()

    return jsonify([p.to_dict() for p in prenotazioni_])

@app.route('/replica/<int:id_replica>', methods=['GET'])
def mostra_replica(id_replica):
    if 'utente_id' not in session:
        return redirect(url_for('login'))

    replica_item = Replica.query.get_or_404(id_replica)
    prenot_utente = Prenotazione.query.filter_by(utente_id=session['utente_id'], replica_id=id_replica).one_or_none()

    if prenot_utente:
        return redirect(url_for('mostra_prenotazione', prenotazione_id=prenot_utente.id))
    return render_template('eventi.html', replica=replica_item)

@app.route('/evento/<int:id_replica>', methods=['POST'])
def nuova_prenotazione(id_replica):
    if 'utente_id' not in session:
        return 'Non sei autorizzato', 401

    quantita = int(request.form.get('quantita'))
    if quantita < 1:
        flash('La quantità deve essere maggiore di zero!', 'warning')
        return redirect(url_for('mostra_replica', id_replica=id_replica))

    replica_item = Replica.query.get_or_404(id_replica)
    if quantita > replica_item.get_qta_disponibile():
        flash('Hai prenotato di più della quantità disponibile.', 'warning')
        return redirect(url_for('mostra_replica', id_replica=id_replica))

    new_prenotazione = Prenotazione(quantita=quantita, replica_id=id_replica, utente_id=session['utente_id'])
    db.session.add(new_prenotazione)
    db.session.commit()
    flash('Prenotazione effettuata con successo!', 'success')

    return redirect(url_for('pag_prenot'))

@app.route('/prenotazione/<int:prenotazione_id>', methods=['POST'])
def modifica_prenotazione(prenotazione_id):
    if 'utente_id' not in session:
        return 'Non sei autorizzato', 401

    prenotazione = Prenotazione.query.get_or_404(prenotazione_id)

    if request.form['azione'] == 'aggiorna':
        nuova_quantita = int(request.form['quantita'])
        if nuova_quantita < 1:
            flash('La quantità deve essere maggiore di zero!', 'warning')
        elif nuova_quantita > prenotazione.rel_repliche.get_qta_disponibile() + prenotazione.quantita:
            flash('Hai prenotato di più della quantità disponibile.', 'warning')
        else:
            prenotazione.quantita = nuova_quantita
            db.session.commit()
            flash('Prenotazione aggiornata con successo!', 'success')
    elif request.form['azione'] == 'elimina':
        db.session.delete(prenotazione)
        db.session.commit()
        flash('Prenotazione eliminata con successo!', 'success')

    return redirect(url_for('pag_prenot'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

