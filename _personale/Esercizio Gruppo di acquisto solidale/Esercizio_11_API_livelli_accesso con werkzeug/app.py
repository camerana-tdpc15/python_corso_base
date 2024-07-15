import os
import locale
import re
from datetime import datetime
from functools import wraps
import shutil
from flask import Flask, flash, g, render_template, jsonify, request, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash, generate_password_hash# Aggiunta questa importazione
from werkzeug.utils import secure_filename
from settings import DATABASE_PATH
from models import db, init_db, Lotto, Prodotto, Produttore, User, Prenotazione

# Imposta la localizzazione italiana per le date
locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)

# Configurazione dell'URI del database e della chiave segreta per l'app Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

# Inizializza l'istanza di SQLAlchemy con l'app Flask
db.init_app(app)  

# Configurazione di Flask-Limiter per limitare il numero di richieste
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

# Funzione per convalidare la password
def is_password_strong(password):
    return (len(password) >= 8 and
            re.search("[a-z]", password) and
            re.search("[A-Z]", password) and
            re.search("[0-9]", password) and
            re.search("[!@#$%^&*(),.?\":{}|<>]", password))

# Configurazione per l'upload dei file
UPLOAD_FOLDER = 'static/imgs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite di 16 MB per l'upload

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configurazione del logging
import logging
logging.basicConfig(level=logging.INFO)

def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return os.path.join('imgs', filename)
    return None

# Listener per l'evento before_request per caricare l'utente loggato
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = User.query.get(user_id) if user_id else None
    if not getattr(g, 'initialized', False):
        create_default_admin()
        g.initialized = True

# Funzione per creare un admin di default se non esiste
def create_default_admin():
    if not User.query.filter_by(email='admin@admin.com').first():
        default_admin = User(
            nome='Admin',
            cognome='Default',
            telefono='0000000000',
            email='admin@admin.com',
            password='Ciotola<1',
            ruolo='admin'
        )
        db.session.add(default_admin)
        db.session.commit()

# Funzioni per il controllo dell'autenticazione come admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user or g.user.ruolo != 'admin':
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Funzione per il controllo dell'autenticazione
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Devi effettuare il login per accedere a questa pagina.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route per la home page
@app.route('/')
def home():
    user = db.session.get(User, session.get('user_id')) if 'user_id' in session else None
    prodotti = Prodotto.query.all()  # Recupera tutti i prodotti
    return render_template('home.html', user=user, prodotti=prodotti)

# API per ottenere i lotti
@app.route('/api/lotti', methods=['GET'])
def get_lotti():
    order = request.args.get('order', 'asc')
    if order not in ['asc', 'desc']:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'
    
    lotti = Lotto.query.order_by(Lotto.data_consegna.desc() if order == 'desc' else Lotto.data_consegna).all()
    return jsonify([lotto.to_dict() for lotto in lotti])

# Route per visualizzare un singolo lotto
@app.route('/lotto/<int:id_lotto>', methods=['GET'])
@login_required
def mostra_lotto(id_lotto):
    lotto = db.session.get(Lotto, id_lotto)
    if not lotto:
        return 'Lotto non trovato!', 404

    prenot_utente = Prenotazione.query.filter_by(
        user_id=session['user_id'],
        lotto_id=id_lotto
    ).first()

    if prenot_utente:
        return redirect(url_for('aggiorna_prenotazione', id_prenotazione=prenot_utente.id))
    else:
        return render_template('lotto.html', lotto=lotto, user=g.user)

# Route per creare una nuova prenotazione
@app.route('/lotto/<int:id_lotto>', methods=['POST'])
@login_required
def nuova_prenotazione(id_lotto):
    try:
        quantita = int(request.form.get('quantita'))
    except ValueError:
        flash('Quantità non valida!', 'warning')
        return redirect(url_for('mostra_lotto', id_lotto=id_lotto))

    lotto = db.session.get(Lotto, id_lotto)
    if not lotto:
        flash('Lotto non trovato!', 'danger')
        return redirect(url_for('home'))

    quantita_disp = lotto.get_qta_disponibile()

    if quantita < 1 or quantita > quantita_disp:
        flash('Quantità non valida.', 'warning')
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

# Route per aggiornare una prenotazione esistente
@app.route('/prenotazione/<int:id_prenotazione>', methods=['GET', 'POST'])
@login_required
@limiter.limit("5 per minute")
def aggiorna_prenotazione(id_prenotazione):
    prenotazione = db.session.get(Prenotazione, id_prenotazione)
    if not prenotazione or prenotazione.user_id != session['user_id']:
        flash('Prenotazione non trovata o non autorizzata!', 'danger')
        return redirect(url_for('mostra_prenotazioni'))

    if request.method == 'POST':
        quantita = int(request.form.get('quantita'))
        lotto = prenotazione.rel_lotto
        quantita_disp = lotto.get_qta_disponibile() + prenotazione.qta

        if quantita < 1 or quantita > quantita_disp:
            flash('Quantità non valida.', 'warning')
            return redirect(url_for('aggiorna_prenotazione', id_prenotazione=id_prenotazione))

        prenotazione.qta = quantita
        db.session.commit()
        flash('Prenotazione aggiornata con successo!', 'success')
        return redirect(url_for('mostra_prenotazioni'))

    return render_template('prenotazione.html', prenotazione=prenotazione, user=g.user)

# Route per visualizzare tutte le prenotazioni dell'utente
@app.route('/prenotazioni')
@login_required
def mostra_prenotazioni():
    return render_template('prenotazioni.html', user=g.user)

# API per ottenere le prenotazioni dell'utente
@app.route('/api/prenotazioni', methods=['GET'])
@login_required
def get_prenotazioni():
    prenotazioni = Prenotazione.query.filter_by(user_id=session['user_id']).all()
    return jsonify([prenotazione.to_dict() for prenotazione in prenotazioni]), 200

# API per modificare una prenotazione
@app.route('/api/prenotazione/modifica', methods=['POST'])
@login_required
def modifica_prenotazione():
    data = request.json
    prenotazione = db.session.get(Prenotazione, data.get('id'))
    if not prenotazione or prenotazione.user_id != session['user_id']:
        return jsonify({"error": "Prenotazione non trovata"}), 404

    try:
        nuova_quantita = int(data.get('quantita'))
    except ValueError:
        return jsonify({"error": "La quantità deve essere un numero intero"}), 400

    lotto = prenotazione.rel_lotto
    quantita_disponibile = lotto.get_qta_disponibile() + prenotazione.qta

    if nuova_quantita < 1 or nuova_quantita > quantita_disponibile:
        return jsonify({"error": f"Quantità non valida. Massimo disponibile: {quantita_disponibile}"}), 400

    prenotazione.qta = nuova_quantita
    db.session.commit()

    return jsonify({"success": True, "message": "Quantità aggiornata con successo"})

# API per eliminare una prenotazione
@app.route('/api/prenotazione/elimina', methods=['POST'])
@login_required
def elimina_prenotazione():
    data = request.json
    prenotazione = db.session.get(Prenotazione, data.get('id'))
    if not prenotazione or prenotazione.user_id != session['user_id']:
        return jsonify({"error": "Prenotazione non trovata"}), 404

    db.session.delete(prenotazione)
    db.session.commit()

    return jsonify({"success": True, "message": "Prenotazione eliminata con successo"})

# Route per il login
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login riuscito!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenziali non valide!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Route per la registrazione
@app.route('/registrazione', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def registrazione():
    if request.method == 'POST':
        if not is_password_strong(request.form['password']):
            flash('La password non soddisfa i requisiti di sicurezza.', 'danger')
            return redirect(url_for('registrazione'))

        if User.query.filter_by(email=request.form['email']).first():
            flash('Email già registrata. Utilizza un\'altra email.', 'danger')
            return render_template('registrazione.html')

        hashed_password = generate_password_hash(request.form['password'])
        new_user = User(
            nome=request.form['nome'],
            cognome=request.form['cognome'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registrazione effettuata con successo. Puoi effettuare il login.', 'success')
        return redirect(url_for('login'))
    return render_template('registrazione.html')

# Route per il logout
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('home'))

# Route per gestire i produttori (aggiunta/modifica) (solo per admin)
@app.route('/gestisci_produttore/<int:id>', methods=['GET', 'POST'])
@app.route('/gestisci_produttore', defaults={'id': None}, methods=['GET', 'POST'])
@admin_required
def gestisci_produttore(id):
    produttore = Produttore.query.get(id) if id else None
    if request.method == 'POST':
        if produttore:
            produttore.nome_produttore = request.form['nome_produttore']
            produttore.descrizione = request.form['descrizione']
            produttore.indirizzo = request.form['indirizzo']
            produttore.telefono = request.form['telefono']
            produttore.email = request.form['email']
            flash('Produttore aggiornato con successo', 'success')
        else:
            nuovo_produttore = Produttore(
                nome_produttore=request.form['nome_produttore'],
                descrizione=request.form['descrizione'],
                indirizzo=request.form['indirizzo'],
                telefono=request.form['telefono'],
                email=request.form['email']
            )
            db.session.add(nuovo_produttore)
            flash('Nuovo produttore aggiunto con successo', 'success')
        
        db.session.commit()
        return redirect(url_for('lista_produttori'))
    
    produttori = Produttore.query.all()
    return render_template('gestisci_produttore.html', produttore=produttore, produttori=produttori)

# Route per gestire i prodotti (aggiunta/modifica) (solo per admin)
@app.route('/gestisci_prodotto/<int:id>', methods=['GET', 'POST'])
@app.route('/gestisci_prodotto', defaults={'id': None}, methods=['GET', 'POST'])
@admin_required
def gestisci_prodotto(id):
    prodotto = Prodotto.query.get(id) if id else None
    if request.method == 'POST':
        try:
            nome_prodotto = request.form['nome_prodotto']
            produttore_id = request.form['produttore_id']
            
            if prodotto:
                prodotto.nome_prodotto = nome_prodotto
                prodotto.produttore_id = produttore_id
            else:
                prodotto = Prodotto(nome_prodotto=nome_prodotto, produttore_id=produttore_id)
                db.session.add(prodotto)
            
            if 'immagine' in request.files:
                file = request.files['immagine']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    upload_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
                    
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)
                    
                    file_path = os.path.join(upload_folder, filename)
                    
                    # Salva il file
                    file.save(file_path)
                    
                    # Verifica che il file sia stato effettivamente salvato
                    if os.path.exists(file_path):
                        prodotto.immagine = os.path.join(filename)
                        app.logger.info(f"File salvato con successo: {file_path}")
                    else:
                        raise Exception(f"Impossibile salvare il file: {file_path}")
                else:
                    app.logger.warning("File non valido o non selezionato")
            
            db.session.commit()
            flash('Prodotto salvato con successo', 'success')
            return redirect(url_for('lista_prodotti'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Errore durante il salvataggio del prodotto: {str(e)}")
            flash(f'Si è verificato un errore durante il salvataggio del prodotto: {str(e)}', 'error')
    
    prodotti = Prodotto.query.all()
    produttori = Produttore.query.all()
    return render_template('gestisci_prodotto.html', prodotto=prodotto, prodotti=prodotti, produttori=produttori)

# Route per gestire i lotti (aggiunta/modifica) (solo per admin)
@app.route('/gestisci_lotto/<int:id>', methods=['GET', 'POST'])
@app.route('/gestisci_lotto', defaults={'id': None}, methods=['GET', 'POST'])
@admin_required
def gestisci_lotto(id):
    lotto = Lotto.query.get(id) if id else None
    if request.method == 'POST':
        if lotto:
            lotto.prodotto_id = request.form['prodotto_id']
            lotto.data_consegna = datetime.strptime(request.form['data_consegna'], '%Y-%m-%d')
            lotto.qta_unita_misura = request.form['qta_unita_misura']
            lotto.qta_lotto = int(request.form['qta_lotto'])
            lotto.prezzo_unitario = float(request.form['prezzo_unitario'])
            lotto.sospeso = request.form['sospeso'] == 'true'
            flash('Lotto aggiornato con successo', 'success')
        else:
            nuovo_lotto = Lotto(
                prodotto_id=request.form['prodotto_id'],
                data_consegna=datetime.strptime(request.form['data_consegna'], '%Y-%m-%d'),
                qta_unita_misura=request.form['qta_unita_misura'],
                qta_lotto=int(request.form['qta_lotto']),
                prezzo_unitario=float(request.form['prezzo_unitario']),
                sospeso=request.form['sospeso'] == 'true'
            )
            db.session.add(nuovo_lotto)
            flash('Nuovo lotto aggiunto con successo', 'success')
        
        db.session.commit()
        return redirect(url_for('lista_lotti'))
    
    lotti = Lotto.query.all()
    prodotti = Prodotto.query.all()
    return render_template('gestisci_lotto.html', lotto=lotto, lotti=lotti, prodotti=prodotti)

# Route per la lista dei produttori (solo per admin)
@app.route('/lista_produttori')
@admin_required
def lista_produttori():
    produttori = Produttore.query.all()
    return render_template('lista_produttori.html', produttori=produttori)

# Route per la lista dei prodotti (solo per admin)
@app.route('/lista_prodotti')
@admin_required
def lista_prodotti():
    prodotti = Prodotto.query.all()
    return render_template('lista_prodotti.html', prodotti=prodotti)

# Route per la lista dei lotti (solo per admin)
@app.route('/lista_lotti')
@admin_required
def lista_lotti():
    lotti = Lotto.query.all()
    return render_template('lista_lotti.html', lotti=lotti)

# Route per gestire gli utenti (solo per admin)
@app.route('/gestisci_utenti', methods=['GET', 'POST'])
@admin_required
def gestisci_utenti():
    if request.method == 'POST':
        user_id = request.form['user_id']
        action = request.form['action']
        user = User.query.get(user_id)
        
        if not user:
            flash('Utente non trovato', 'danger')
        elif action == 'update':
            user.ruolo = request.form['ruolo']
            db.session.commit()
            flash('Ruolo aggiornato con successo', 'success')
        elif action == 'delete':
            if Prenotazione.query.filter_by(user_id=user_id).count() > 0:
                flash('Impossibile eliminare l\'utente, ci sono delle prenotazioni!', 'danger')
            else:
                db.session.delete(user)
                db.session.commit()
                flash('Utente eliminato con successo', 'success')
    
    utenti = User.query.all()
    return render_template('gestisci_utenti.html', utenti=utenti)

# Inizializzazione dell'app e del database
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)