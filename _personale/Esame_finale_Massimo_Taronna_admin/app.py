import re
import locale
from functools import wraps
from flask import Flask, flash, g, render_template, jsonify, request, session, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import check_password_hash
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
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "100 per hour"])

# Funzione per convalidare l'efficacia della password
def is_password_strong(password):
    return (len(password) >= 8 and
            re.search("[a-z]", password) and
            re.search("[A-Z]", password) and
            re.search("[0-9]", password) and
            re.search("[!@#$%^&*(),.?\":{}|<>]", password))

# Configurazione Flask-Admin
class AdminModelView(ModelView):
    def is_accessible(self):
        print("Checking access:", session.get('logged_in'), session.get('role'))
        return session.get('logged_in') and session.get('role') == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        print("Inaccessible callback called")
        return redirect(url_for('login'))

admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
admin.add_view(AdminModelView(Locale, db.session))
admin.add_view(AdminModelView(Evento, db.session))
admin.add_view(AdminModelView(Replica, db.session))
admin.add_view(AdminModelView(Utente, db.session))

# Carica l'utente loggato prima di ogni richiesta
@app.before_request
def load_logged_in_user():
    utente_id = session.get('utente_id')
    if utente_id is None:
        g.user = None
    else:
        g.user = Utente.query.get(utente_id)

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
    return render_template('home.html')

# Route per la pagina dei Luoghi
@app.route('/luoghi')
def luoghi():
    return render_template('luoghi.html')

# API per ottenere gli eventi con repliche e posti disponibili
@app.route('/api/eventi_con_repliche', methods=['GET'])
def get_eventi_con_repliche():
    eventi = Evento.query.all()
    eventi_data = [evento.to_dict_with_details() for evento in eventi]
    return jsonify(eventi_data)

# Route per visualizzare una singola replica
@app.route('/replica/<int:id_replica>', methods=['GET'])
@login_required
def mostra_replica(id_replica):
    replica = db.session.get(Replica, id_replica)
    if not replica:
        return 'Replica non trovata!', 404

    prenot_utente = Prenotazione.query.filter_by(
        utente_id=session['utente_id'],
        replica_id=id_replica
    ).first()

    if prenot_utente:
        return redirect(url_for('aggiorna_prenotazione', id_prenotazione=prenot_utente.id))
    else:
        return render_template('replica.html', replica=replica, utente=g.user)

# Route per prenotare una replica
@app.route('/prenota/<int:replica_id>', methods=['POST'])
@login_required
def prenota_replica(replica_id):
    data = request.json
    # posti prenotati
    quantita = data.get('quantita', 1)
    replica = Replica.query.get_or_404(replica_id)

    if replica.annullato:
        return jsonify({'error': 'Replica annullata, non prenotabile.'}), 400

    # Controlla se l'utente ha già una prenotazione per questa replica
    prenotazione = Prenotazione.query.filter_by(utente_id=g.user.id, replica_id=replica_id).first()
    if prenotazione:
        return jsonify({'error': 'Hai già una prenotazione per questa replica. Puoi modificarla nella pagina delle prenotazioni.'}), 400

    # Se non esiste una prenotazione, creane una nuova
    nuova_prenotazione = Prenotazione(utente_id=g.user.id, replica_id=replica.id, quantita=quantita)
    db.session.add(nuova_prenotazione)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Prenotazione effettuata con successo!'})

# API per ottenere le prenotazioni dell'utente
@app.route('/api/prenotazioni', methods=['GET'])
@login_required
def get_prenotazioni():
    prenotazioni = Prenotazione.query.filter_by(utente_id=g.user.id).all()
    return jsonify([prenotazione.to_dict() for prenotazione in prenotazioni])

# API per modificare una prenotazione
@app.route('/api/prenotazioni/<int:prenotazione_id>', methods=['PUT'])
@login_required
def modifica_prenotazione(prenotazione_id):
    data = request.json
    prenotazione = Prenotazione.query.get_or_404(prenotazione_id)
    if prenotazione.utente_id != g.user.id:
        return jsonify({'error': 'Non autorizzato'}), 403
    prenotazione.quantita = data.get('quantita', prenotazione.quantita)
    db.session.commit()
    return jsonify(prenotazione.to_dict())

# API per cancellare una prenotazione
@app.route('/api/prenotazioni/<int:prenotazione_id>', methods=['DELETE'])
@login_required
def cancella_prenotazione(prenotazione_id):
    prenotazione = Prenotazione.query.get_or_404(prenotazione_id)
    if prenotazione.utente_id != g.user.id:
        return jsonify({'error': 'Non autorizzato'}), 403
    db.session.delete(prenotazione)
    db.session.commit()
    return jsonify({'success': True})

# Route per visualizzare la pagina delle prenotazioni
@app.route('/prenotazioni')
@login_required
def mostra_prenotazioni():
    return render_template('prenotazioni.html')

@app.route('/api/replica/<int:replica_id>/data_formattata', methods=['GET'])
def get_data_formattata(replica_id):
    replica = Replica.query.get_or_404(replica_id)
    return jsonify({'data_formattata': replica.get_date()})

# Route per il login
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        utente = Utente.query.filter_by(email=email).first()
        if utente:
            if check_password_hash(utente.password, password):
                session['utente_id'] = utente.id
                session['role'] = utente.ruolo
                session['logged_in'] = True  # Aggiungi questa riga
                flash('Login effettuato!', 'success')
                if utente.ruolo == 'admin':
                    return redirect(url_for('admin.index'))
                else:
                    return redirect(url_for('home'))
            else:
                flash('Password errata!', 'danger')
        else:
            flash('Email non trovata!', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

# Route per la registrazione di un nuovo utente
# La password viene hashata in models.py
@app.route('/registrazione', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def registrazione():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not is_password_strong(password):
            flash('La password non soddisfa i requisiti di sicurezza.', 'danger')
            return redirect(url_for('registrazione'))
        
        if Utente.query.filter_by(email=email).first():
            flash('Email già registrata. Utilizza un\'altra email.', 'danger')
            return render_template('registrazione.html')
    
        nuovo_utente = Utente(
            cognome=request.form['cognome'],
            nome=request.form['nome'],
            telefono=request.form['telefono'],
            email=email,
            password=password
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
    session.pop('utente_id', None)
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('home'))

# Inizializzazione dell'app e del database
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)