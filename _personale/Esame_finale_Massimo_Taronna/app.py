import os
import re
import locale
from functools import wraps
from datetime import datetime
from flask import Flask, flash, g, render_template, jsonify, request, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from settings import DATABASE_PATH
from models import db, init_db, Utente, Prenotazione, Replica, Evento, Locale

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

# Listener per l'evento before_request per caricare l'utente loggato
@app.before_request
def load_logged_in_user():
    utente_id = session.get('utente_id')
    g.utente = Utente.query.get(utente_id) if utente_id else None
    if not getattr(g, 'initialized', False):
        g.initialized = True

# Funzione per il controllo dell'autenticazione
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'utente_id' not in session:
            flash('Devi effettuare il login per accedere a questa pagina.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route per la home page
@app.route('/')
def home():
    utente = db.session.get(Utente, session.get('utente_id')) if 'utente_id' in session else None
    eventi = Evento.query.all()  # Recupera tutti gli eventi
    return render_template('home.html', utente=utente, eventi=eventi)

# API per ottenere le repliche
@app.route('/api/repliche', methods=['GET'])
def get_repliche():
    order = request.args.get('order', 'asc')
    if order not in ['asc', 'desc']:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'
    
    repliche = Replica.query.order_by(Replica.data_ora.desc() if order == 'desc' else Replica.data_ora).all()
    return jsonify([replica.to_dict() for replica in repliche])

# Route per visualizzare una singola replica
@app.route('/replica/<int:id_replica>', methods=['GET'])
@login_required
def mostra_replica(id_replica):
    replica = db.session.get(Replica, id_replica)
    if not replica:
        return 'Replica non trovato!', 404

    prenot_utente = Prenotazione.query.filter_by(
        utente_id=session['utente_id'],
        replica_id=id_replica
    ).first()

    if prenot_utente:
        return redirect(url_for('aggiorna_prenotazione', id_prenotazione=prenot_utente.id))
    else:
        return render_template('replica.html', replica=replica, utente=g.utente)



# Route per il login
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        utente = Utente.query.filter_by(email=email).first()
        if utente and check_password_hash(utente.password, password):
            session['utente_id'] = utente.id
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

        if Utente.query.filter_by(email=request.form['email']).first():
            flash('Email già registrata. Utilizza un\'altra email.', 'danger')
            return render_template('registrazione.html')

        hashed_password = generate_password_hash(request.form['password'])
        nuovo_utente = Utente(
            cognome=request.form['cognome'],
            nome=request.form['nome'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            password=hashed_password
        )
        db.session.add(nuovo_utente)
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


# Inizializzazione dell'app e del database
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)