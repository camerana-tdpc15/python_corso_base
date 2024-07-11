import locale
import re
from datetime import datetime
from functools import wraps
from flask import Flask, flash, g, render_template, jsonify, request, session, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from settings import DATABASE_PATH
from models import db, init_db, Lotto, Prodotto, Produttore, User, Prenotazione

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

# Configurazione di Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Funzione per convalidare la password
def is_password_strong(password):
    """Controlla se la password soddisfa i criteri di sicurezza."""
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Listener per l'evento first_request per creare l'admin di default
@app.before_request
def before_request():
    if not hasattr(g, 'initialized'):
        create_default_admin()
        g.initialized = True

def create_default_admin():
    if not User.query.filter_by(email='admin@admin.com').first():
        hashed_password = bcrypt.generate_password_hash('Ciotola_1').decode('utf-8')
        default_admin = User(
            nome='Admin',
            cognome='Default',
            telefono='0000000000',
            email='admin@admin.com',
            password=hashed_password,
            ruolo='admin'
        )
        db.session.add(default_admin)
        db.session.commit()

# Funzioni per il controllo dei ruoli
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user or g.user.ruolo != 'admin':
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Decoratore per proteggere le rotte che richiedono autenticazione
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Devi effettuare il login per accedere a questa pagina.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# Mostra l'elenco dei lotti disponibili
@app.route('/')
def home():
    user = None
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
    return render_template('home.html', user=user)

# Restituisce i dati dei lotti disponibili in formato JSON
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


@app.route('/lotto/<int:id_lotto>', methods=['GET']) # verifico che sia un integer
@login_required
def mostra_lotto(id_lotto): #endpoint
    # Controllare che l'utente sia loggato
    if 'user_id' not in session:
        return redirect(url_for('login'))


    # Ottengo il record del lotto a partire dal suo ID
    lotto = db.session.get(Lotto, id_lotto)
    if not lotto:
        return 'Lotto non trovato!', 404

    prenot_utente = Prenotazione.query.filter_by(
        user_id=session['user_id'],
        lotto_id=id_lotto
    ).first()           # se uso all ottengo una lista, meglio usare first o one

    # Se l'utente ha delle prenotazioni su qusto specifico lotto
    if prenot_utente:
        return redirect(url_for('aggiorna_prenotazione', id_prenotazione=prenot_utente.id))
    # Se l'utente non ha delle prenotazioni su questo specifico lotto
    else:
        return render_template('lotto.html', lotto=lotto, user=g.user)
    
@app.route('/lotto/<int:id_lotto>', methods=['POST'])
def nuova_prenotazione(id_lotto):
    if 'user_id' not in session:
        return 'non sei autorizzato', 401
    else:       # istruzione inutile a livello di programma, ma esplicita che se non sei loggato non puoi continuare
        pass
    
    quantita = request.form.get('quantita')
    try:
        quantita = int(quantita)
    except ValueError:
        flash('Quantità non valida!', 'warning')
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))

     # Ottieni l'oggetto Lotto dal database 
    lotto = db.session.get(Lotto, id_lotto)
    if not lotto:
        flash('Lotto non trovato!', 'danger')
        return redirect(url_for('home'))

    # Ottieni la quantità disponibile dal metodo dell'oggetto Lotto
    quantita_disp = lotto.get_qta_disponibile()

    # verifica che la quantità sia 
    #   - minore o uguale alla quantità disponibile
    #   - che sia un valore > o = a 1
    if quantita < 1:
        flash('La quantità deve essere maggiore di 0', 'warning')
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))
    
    if quantita > quantita_disp:
        flash('La quantità deve essere minore o uguale a quella disponibile', 'warning')
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))

    new_prenotazione = Prenotazione(qta=quantita, lotto_id=id_lotto, user_id=session['user_id'])
    db.session.add(new_prenotazione)
    try:
        db.session.commit()
        flash('Prenotazione effettuata con successo!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Errore durante la prenotazione. Riprovare.', 'danger')
        print(f"Error: {e}")

    return redirect(url_for('mostra_prenotazioni'))

@app.route('/prenotazione/<int:id_prenotazione>', methods=['GET', 'POST'])
@login_required
@limiter.limit("5 per minute")
def aggiorna_prenotazione(id_prenotazione):
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Non sei autorizzato', 'danger')
        return redirect(url_for('login'))

    # Fetch dei dettagli della prenotazione
    prenotazione = db.session.get(Prenotazione, id_prenotazione)
    if not prenotazione:
        flash('Prenotazione non trovata!', 'danger')
        return redirect(url_for('mostra_prenotazioni'))

    # Verificare che l'utente loggato è autorizzato a modificare la prenotazione
    if prenotazione.user_id != session['user_id']:
        flash('Non sei autorizzato a modificare questa prenotazione', 'danger')
        return redirect(url_for('mostra_prenotazioni'))

    if request.method == 'POST':
        quantita = int(request.form.get('quantita'))
        # Fetch al lotto associato
        lotto = db.session.get(Lotto, prenotazione.lotto_id)
        if not lotto:
            flash('Lotto non trovato!', 'danger')
            return redirect(url_for('mostra_prenotazioni'))

        quantita_disp = lotto.get_qta_disponibile()

        if quantita < 1:
            flash('La quantità deve essere maggiore di 0', 'warning')
            return redirect(url_for('aggiorna_prenotazione', id_prenotazione=id_prenotazione))

        if quantita > quantita_disp + prenotazione.qta:
            flash('La quantità deve essere minore o uguale a quella disponibile', 'warning')
            return redirect(url_for('aggiorna_prenotazione', id_prenotazione=id_prenotazione))

        prenotazione.qta = quantita
        db.session.commit()
        flash('Prenotazione aggiornata con successo!', 'success')
        return redirect(url_for('mostra_prenotazioni'))

    return render_template('prenotazione.html', prenotazione=prenotazione, user=g.user)

    
@app.route('/prenotazioni')
@login_required
def mostra_prenotazioni():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = None                                               # ho aggiunto g. vedere se da dei problemi
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])       # ho aggiunto g. vedere se da dei problemi
    return render_template('prenotazioni.html', user=g.user)    # qui g. c'era già

@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    if 'user_id' not in session:
        return jsonify({"error": "Non sei autorizzato"}), 401
    
    # fetch alle prenotazioni dell'utente
    user_id = session['user_id']
    prenotazioni = Prenotazione.query.filter_by(user_id=user_id).all()

    # controllo se ci sono altre prenotazioni
    if not prenotazioni:
        return jsonify([]), 200
    
    # Uso SerializerMixin per generare la lista prenotazioni
    prenotazioni_list = [prenotazione.to_dict() for prenotazione in prenotazioni]
    
    return jsonify(prenotazioni_list), 200

@app.route('/api/prenotazione/modifica', methods=['POST'])
def modifica_prenotazione():
    if 'user_id' not in session:
        return jsonify({"error": "Non sei autorizzato"}), 401
    
    data = request.json
    prenotazione_id = data.get('id')
    try:
        nuova_quantita = int(data.get('quantita'))
    except ValueError:
        return jsonify({"error": "La quantità deve essere un numero intero"}), 400
    
    prenotazione = Prenotazione.query.get(prenotazione_id)
    if not prenotazione or prenotazione.user_id != session['user_id']:
        return jsonify({"error": "Prenotazione non trovata"}), 404
    
    lotto = prenotazione.rel_lotto
    quantita_disponibile = lotto.get_qta_disponibile() + prenotazione.qta
    
    if nuova_quantita > quantita_disponibile:
        return jsonify({"error": f"Quantità non disponibile. Massimo disponibile: {quantita_disponibile}"}), 400
    
    if nuova_quantita <1:
        return jsonify({"error": "La quantità deve essere maggiore di zero"}), 400
    
    prenotazione.qta = nuova_quantita
    db.session.commit()
    
    return jsonify({"success": True, "message": "Quantità aggiornata con successo"})

@app.route('/api/prenotazione/elimina', methods=['POST'])
def elimina_prenotazione():
    if 'user_id' not in session:
        return jsonify({"error": "Non sei autorizzato"}), 401
    
    data = request.json
    prenotazione_id = data.get('id')
    
    prenotazione = Prenotazione.query.get(prenotazione_id)
    if not prenotazione or prenotazione.user_id != session['user_id']:
        return jsonify({"error": "Prenotazione non trovata"}), 404
    
    db.session.delete(prenotazione)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Prenotazione eliminata con successo"})

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
       
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login riuscito!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenziali non valide!', 'danger')
            return redirect(url_for('login'))
    
    elif request.method == 'GET':
        return render_template('login.html')
    
@app.route('/registrazione', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def registrazione():
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        telefono = request.form['telefono']
        email = request.form['email']
        password = request.form['password']

        if not is_password_strong(password):
            flash('La password deve contenere almeno 8 caratteri, incluse lettere maiuscole, minuscole, numeri e caratteri speciali.', 'danger')
            return redirect(url_for('registrazione'))

        # Hashing della password con bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Verifica se l'email esiste già
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email già registrata. Utilizza un\'altra email.', 'danger')
            return render_template('registrazione.html')
        
        new_user = User(nome=nome, cognome=cognome, telefono=telefono, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrazione effettuata con successo. Puoi effettuare il login.', 'success')
        return redirect(url_for('login'))
    return render_template('registrazione.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('home'))

# funzioni per amministratore
@app.route('/nuovo_produttore', methods=['GET', 'POST'])
@admin_required
def nuovo_produttore():
    if request.method == 'POST':
        nome_produttore = request.form['nome_produttore']
        descrizione = request.form['descrizione']
        indirizzo = request.form['indirizzo']
        telefono = request.form['telefono']
        email = request.form['email']
        nuovo_produttore = Produttore(
            nome_produttore=nome_produttore, 
            descrizione=descrizione, 
            indirizzo=indirizzo, 
            telefono=telefono, 
            email=email)
        db.session.add(nuovo_produttore)
        db.session.commit()
        flash('Produttore aggiunto con successo', 'success')
        return redirect(url_for('home'))
    return render_template('nuovo_produttore.html')

@app.route('/nuovo_prodotto', methods=['GET', 'POST'])
@admin_required
def nuovo_prodotto():
    produttori = Produttore.query.all()
    if request.method == 'POST':
        produttore_id = request.form['produttore_id']
        nome_prodotto = request.form['nome_prodotto']
        immagine = request.form['immagine']
        nuovo_prodotto = Prodotto(
            produttore_id=produttore_id, 
            nome_prodotto=nome_prodotto, 
            immagine=immagine)
        db.session.add(nuovo_prodotto)
        db.session.commit()
        flash('Prodotto aggiunto con successo', 'success')
        return redirect(url_for('home'))
    return render_template('nuovo_prodotto.html', produttori=produttori)

@app.route('/nuovo_lotto', methods=['GET', 'POST'])
@admin_required
def nuovo_lotto():
    prodotti = Prodotto.query.all()
    if request.method == 'POST':
        prodotto_id = request.form['prodotto_id']
        data_consegna = datetime.strptime(request.form['data_consegna'], '%Y-%m-%d')
        qta_unita_misura = request.form['qta_unita_misura']
        qta_lotto = request.form['qta_lotto']
        prezzo_unitario = request.form['prezzo_unitario']
        sospeso = request.form['sospeso'] == 'true'
        nuovo_lotto = Lotto(
            prodotto_id=prodotto_id, 
            data_consegna=data_consegna, 
            qta_unita_misura=qta_unita_misura, 
            qta_lotto=qta_lotto, 
            prezzo_unitario=prezzo_unitario, 
            sospeso=sospeso)
        db.session.add(nuovo_lotto)
        db.session.commit()
        flash('Lotto aggiunto con successo', 'success')
        return redirect(url_for('home'))
    return render_template('nuovo_lotto.html', prodotti=prodotti)

@app.route('/gestisci_utenti', methods=['GET', 'POST'])
@admin_required
def gestisci_utenti():
    if request.method == 'POST':
        user_id = request.form['user_id']
        action = request.form['action']
        
        if action == 'update':
            nuovo_ruolo = request.form['ruolo']
            utente = User.query.get(user_id)
            if utente:
                utente.ruolo = nuovo_ruolo
                db.session.commit()
                flash('Ruolo aggiornato con successo', 'success')
        elif action == 'delete':
            utente = User.query.get(user_id)
            if utente:
                prenotazioni = Prenotazione.query.filter_by(user_id=user_id).count()
                if prenotazioni > 0:
                    flash('Impossibile eliminare l\'utente, ci sono delle prenotazioni!', 'danger')
                else:
                    db.session.delete(utente)
                    db.session.commit()
                    flash('Utente eliminato con successo', 'success')
    
    utenti = User.query.all()
    return render_template('gestisci_utenti.html', utenti=utenti)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)