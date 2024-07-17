import locale as loc
from flask import Flask, flash, render_template, jsonify, request, session, redirect, url_for
from models import db, init_db, Prenotazione, Utente, Replica, Evento, Locale
from settings import DATABASE_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH  # Configura il percorso del database SQLite
app.config['SECRET_KEY'] = 'mysecretkey'  # Chiave segreta per gestire le sessioni e i messaggi flash

db.init_app(app)  # Inizializza l'app Flask con il database

# Route per la pagina iniziale che reindirizza alla pagina di login
@app.route('/')
def iniziale():
    return redirect(url_for('login'))

# Route per la home page
@app.route('/home')
def home():
    return render_template('home.html')

# Route per la pagina delle prenotazioni
@app.route('/prenotazioni', methods=['GET'])
def pag_prenot():
    if 'utente_id' not in session:  # Verifica se l'utente è loggato
        return redirect(url_for('login'))

    prenotazioni_ = Prenotazione.query \
        .filter_by(utente_id=session['utente_id']) \
        .join(Replica, Replica.id == Prenotazione.replica_id) \
        .order_by(Replica.data_ora) \
        .all()  # Recupera le prenotazioni dell'utente ordinandole per data e ora

    return render_template('Prenotazioni.html', prenotazioni=prenotazioni_)

# Route per la pagina degli eventi
@app.route('/eventi')
def pag_eventi():
    if 'utente_id' not in session:  # Verifica se l'utente è loggato
        return redirect(url_for('login'))

    eventi = Evento.query.all()  # Recupera tutti gli eventi
    repliche = Replica.query.all()  # Recupera tutte le repliche
    return render_template('eventi.html', eventi=eventi, repliche=repliche)

# Route per il login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Gestisce il form di login
        email = request.form.get('email')
        password = request.form.get('password')
        user = Utente.query.filter_by(email=email, password=password).one_or_none()  # Verifica le credenziali
        if user:
            session['utente_id'] = user.id  # Salva l'ID dell'utente nella sessione
            flash('Login riuscito!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenziali non valide!', 'warning')
            return redirect(url_for('login'))
    return render_template('login.html')

# Route per il logout
@app.route('/logout')
def logout():
    session.pop('utente_id', None)  # Rimuove l'ID dell'utente dalla sessione
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('login'))

# API per ottenere le repliche degli eventi ordinati
@app.route('/api/eventi', methods=['GET'])
def get_eventi():
    order = request.args.get('order', 'asc')  # Recupera il parametro di ordinamento (asc o desc)
    if order not in ['asc', 'desc']:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".', 400

    order_by = Replica.data_ora.asc() if order == 'asc' else Replica.data_ora.desc()
    repliche = Replica.query.order_by(order_by).all()  # Ordina le repliche

    return jsonify([r.to_dict() for r in repliche])  # Restituisce le repliche in formato JSON

# API per ottenere le prenotazioni dell'utente loggato
@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    if 'utente_id' not in session:  # Verifica se l'utente è loggato
        return redirect(url_for('login'))

    prenotazioni_ = Prenotazione.query \
        .filter_by(utente_id=session['utente_id']) \
        .join(Replica, Replica.id == Prenotazione.replica_id) \
        .order_by(Replica.data_ora) \
        .all()  # Recupera le prenotazioni dell'utente

    return jsonify([p.to_dict() for p in prenotazioni_])  # Restituisce le prenotazioni in formato JSON

# Route per mostrare i dettagli di una replica
@app.route('/replica/<int:id_replica>', methods=['GET'])
def mostra_replica(id_replica):
    if 'utente_id' not in session:  # Verifica se l'utente è loggato
        return redirect(url_for('login'))

    replica_item = Replica.query.get_or_404(id_replica)  # Recupera la replica specifica
    prenot_utente = Prenotazione.query.filter_by(utente_id=session['utente_id'], replica_id=id_replica).one_or_none()

    if prenot_utente:  # Se l'utente ha già prenotato questa replica, reindirizza alla pagina della prenotazione
        return redirect(url_for('mostra_prenotazione', prenotazione_id=prenot_utente.id))
    return render_template('eventi.html', replica=replica_item)

# Route per creare una nuova prenotazione
@app.route('/evento/<int:id_replica>', methods=['POST'])
def nuova_prenotazione(id_replica):
    if 'utente_id' not in session:  # Verifica se l'utente è loggato
        return 'Non sei autorizzato', 401

    quantita = int(request.form.get('quantita'))  # Recupera la quantità dal form
    if quantita < 1:
        flash('La quantità deve essere maggiore di zero!', 'warning')
        return redirect(url_for('mostra_replica', id_replica=id_replica))

    replica_item = Replica.query.get_or_404(id_replica)
    if quantita > replica_item.get_qta_disponibile():
        flash('Hai prenotato di più della quantità disponibile.', 'warning')
        return redirect(url_for('pag_eventi'))

    new_prenotazione = Prenotazione(quantita=quantita, replica_id=id_replica, utente_id=session['utente_id'])  # Crea una nuova prenotazione
    db.session.add(new_prenotazione)
    db.session.commit()
    flash('Prenotazione effettuata con successo!', 'success')

    return redirect(url_for('pag_prenot'))

# Route per modificare o eliminare una prenotazione
@app.route('/prenotazione/<int:prenotazione_id>', methods=['POST'])
def modifica_prenotazione(prenotazione_id):
    if 'utente_id' not in session:  # Verifica se l'utente è loggato
        return 'Non sei autorizzato', 401

    prenotazione = Prenotazione.query.get_or_404(prenotazione_id)  # Recupera la prenotazione specifica

    if request.form['azione'] == 'aggiorna':
        nuova_quantita = int(request.form['quantita'])
        if nuova_quantita < 1:
            flash('La quantità deve essere maggiore di zero!', 'warning')
        elif nuova_quantita > prenotazione.rel_repliche.get_qta_disponibile() + prenotazione.quantita:
            flash('Hai prenotato di più della quantità disponibile.', 'warning')
        else:
            prenotazione.quantita = nuova_quantita  # Aggiorna la quantità della prenotazione
            db.session.commit()
            flash('Prenotazione aggiornata con successo!', 'success')
    elif request.form['azione'] == 'elimina':
        db.session.delete(prenotazione)  # Elimina la prenotazione
        db.session.commit()
        flash('Prenotazione eliminata con successo!', 'success')

    return redirect(url_for('pag_prenot'))

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Inizializza il database se non è già stato fatto
    app.run(debug=True)  # Avvia l'app in modalità di debug
