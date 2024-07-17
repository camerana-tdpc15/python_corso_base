from functools import wraps
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from sqlalchemy import func
from models import Utente, Replica, Prenotazione, Evento, Locale, db, init_db
from settings import DATABASE_PATH

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,
    
)

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask


# creo funzione per controllo del utente loggato
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'utente_id' not in session:
            flash('Per favore, effettua il login per accedere a questa pagina.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Mostra la pagina che deve elencare i lotti disponibili

@app.route('/')
def index():
    eventi = Evento.query.all()
    eventi_data = []
    for evento in eventi:
        repliche_data = []
        for replica in evento.rel_repliche:
            posti_prenotati = db.session.query(func.sum(Prenotazione.quantita)).filter_by(replica_id=replica.id).scalar() or 0
            posti_disponibili = evento.rel_locale.posti - posti_prenotati
            repliche_data.append({
                'id': replica.id,
                'data_ora': replica.data_ora,
                'annullato': replica.annullato,
                'posti_disponibili': posti_disponibili
                
            })
        eventi_data.append({
            'id': evento.id,
            'nome_evento': evento.nome_evento,
            'locale': evento.rel_locale.nome_locale,
            'repliche': repliche_data,
            'immagine': evento.immagine
        })
    return render_template('index.html', eventi=eventi_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        utente = Utente.query.filter_by(email=email).first()

        if utente and utente.password == password:
            session['utente_id'] = utente.id
            flash(f'Login riuscito. Benvenuto {utente.nome}!', 'success')
            return redirect(url_for('prenotazioni'))
        else:
            flash('Login non riuscito. Controlla email e password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
# chiamo funzione controllo login
@login_required
def logout():
    session.clear()
    flash('Logout effettuato con successo.', 'success')
    return redirect(url_for('login'))



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        cognome = request.form.get("cognome")
        nome = request.form.get("nome")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        password = request.form.get("password")
        if not cognome or not nome or not telefono or not email or not password:
            flash("Tutti i campi sono obbligatori!", "danger")
            return redirect(url_for("signup"))
        if (
            Utente.query.filter_by(nome=nome).first()
            or Utente.query.filter_by(cognome=cognome).first()
            or Utente.query.filter_by(email=email).first()
        ):
            flash("Il nome o il cognome o l'email sono già in uso!", "danger")
            return redirect(url_for("signup"))
        nuovo_utente = Utente(cognome=cognome, nome=nome, telefono=telefono, email=email, password=password)
        db.session.add(nuovo_utente)
        db.session.commit()
        flash("Registrazione effettuata con successo!", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route('/api/repliche/<int:evento_id>')
def get_repliche(evento_id):
    # cerca un evento nel database con l'ID specificato
    evento = Evento.query.get_or_404(evento_id)
    # prepara delle informazioni sulle repliche
    repliche = []
    for replica in evento.rel_repliche:
        # calcola posti_prenotati per quella replica
        posti_prenotati = db.session.query(func.sum(Prenotazione.quantita)).filter_by(replica_id=replica.id).scalar() or 0
        # calcola posti_disponibili per quella replica
        posti_disponibili = evento.rel_locale.posti - posti_prenotati
        # per ogni replica, crea un dizionario con...
        repliche.append({
            'id': replica.id,
            'data_ora': replica.data_ora.strftime('%d-%m-%Y %H:%M'),
            'annullato': replica.annullato,
            'posti_disponibili': posti_disponibili
        })
    # trasformo tale dizionario in json    
    return jsonify({
        'nome_evento': evento.nome_evento,
        'locale': evento.rel_locale.nome_locale,
        'luogo': evento.rel_locale.luogo,
        'repliche': repliche
    })

# mostra le repliche di un evento specifico    
@app.route('/repliche/<int:evento_id>')
@login_required
def repliche(evento_id):
    return render_template('repliche.html', evento_id=evento_id)

# prenotazione REPLICA
@app.route('/prenota', methods=['POST'])
# controllo login
@login_required
# si ottengono i dati JSON inviati
def prenota():
    # contiene i dati JSON inviati con la richiesta POST
    data = request.json
    # questi invece vengono estratti dai dati JSON
    replica_id = data.get('replica_id')
    # quantita è opzionale se non specificato rimane 1
    quantita = int(data.get('quantita', 1))
    
    # ottengo replica facendo riferimento a replica_id
    replica = Replica.query.get_or_404(replica_id)
    if replica.annullato:
        return jsonify({'error': 'Questa replica è stata annullata.'}), 400
    
    # creo un nuovo oggetto prenotazione
    prenotazione = Prenotazione(utente_id=session['utente_id'], replica_id=replica_id, quantita=quantita)
    db.session.add(prenotazione)
    db.session.commit()
    
    return jsonify({'message': 'Prenotazione effettuata con successo!'}), 201

# prenotazione EVENTO
@app.route('/api/prenotazioni', methods=['GET', 'POST'])
@login_required
def api_prenotazioni():
    # Quando la richiesta è di tipo GET, l'API restituisce tutte le prenotazioni dell'utente corrente
    if request.method == 'GET':
        prenotazioni = Prenotazione.query.filter_by(utente_id=session['utente_id']).all()
        prenotazioni_data = []
        for p in prenotazioni:
            prenotazioni_data.append({
                'id': p.id,
                'evento': p.rel_replica.rel_evento.nome_evento,
                'locale': p.rel_replica.rel_evento.rel_locale.nome_locale,
                'data_ora': p.rel_replica.data_ora.strftime('%d-%m-%Y %H:%M'),
                'quantita': p.quantita,
                'annullato': p.rel_replica.annullato,
                'replica_id': p.replica_id
                
            })
        return jsonify(prenotazioni_data)
    
    # Quando la richiesta è di tipo POST, l'API gestisce azioni come creare, aggiornare o cancellare una prenotazione.
    elif request.method == 'POST':
        data = request.json
        action = data.get('action')
        
        # creazione di una nuova prenotazione
        if action == 'create':
            # recupero i dati
            replica_id = data.get('replica_id')
            quantita = data.get('quantita', 1)
            
            # Controllo prenotazione esistente
            existing_prenotazione = Prenotazione.query.filter_by(utente_id=session['utente_id'], replica_id=replica_id).first()
            # se la prenotazione è già esistente
            if existing_prenotazione:
                return jsonify({'error': 'Hai già una prenotazione per questa replica.'}), 400
            
            # se la replica è stata annullata
            replica = Replica.query.get_or_404(replica_id)
            if replica.annullato:
                return jsonify({'error': 'Questa replica è stata annullata.'}), 400
            
            # altrimenti si procede con la Creazione della prenotazione:
            prenotazione = Prenotazione(utente_id=session['utente_id'], replica_id=replica_id, quantita=quantita)
            db.session.add(prenotazione)
            db.session.commit()
            
            return jsonify({'message': 'Prenotazione effettuata con successo!'}), 201
        
        # modifica prenotazione esistente
        elif action == 'update':
            # recupera i dati
            prenotazione_id = data.get('prenotazione_id')
            nuova_quantita = data.get('quantita')
            
            # Viene recuperata la prenotazione dal database tramite l'ID specificato 
            prenotazione = Prenotazione.query.get_or_404(prenotazione_id)
            # verifica se l'utente corrente (identificato da session['uyente_id']) è uguale a quello associato alla prenotazione
            if prenotazione.utente_id != session['utente_id']:
                return jsonify({'error': 'Non sei autorizzato a modificare questa prenotazione.'}), 403
            
            #  se la replica associata alla prenotazione è stata annullata
            if prenotazione.rel_replica.annullato:
                return jsonify({'error': 'Questa replica è stata annullata.'}), 400
            
            # Aggiornamento della quantità della prenotazione
            prenotazione.quantita = nuova_quantita
            db.session.commit()
            
            return jsonify({'message': 'Prenotazione aggiornata con successo!'})
        
        # cancella prenotazione
        elif action == 'delete':
            # Recupero dei dati estratto dai dati JSON ricevuti.
            prenotazione_id = data.get('prenotazione_id')
            # Recupero della prenotazione esistente dal database utilizzando l'ID specificato 
            prenotazione = Prenotazione.query.get_or_404(prenotazione_id)
            
            # Controllo di autorizzazione
            if prenotazione.utente_id != session['utente_id']:
                return jsonify({'error': 'Non sei autorizzato a cancellare questa prenotazione.'}), 403
            
            # Cancellazione della prenotazione
            db.session.delete(prenotazione)
            db.session.commit()
            
            return jsonify({'message': 'Prenotazione cancellata con successo!'})
        
        else:
            return jsonify({'error': 'Azione non valida'}), 400
        
# visualizza le prenotazioni
@app.route('/prenotazioni')
@login_required
def prenotazioni():
    return render_template('prenotazioni.html')


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
