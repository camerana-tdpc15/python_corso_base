import locale
import hashlib
from flask import Flask, flash, redirect, render_template, jsonify, request, session, url_for
from models import Prenotazione, User, db, init_db, Lotto, Prodotto, Produttore
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,
    DEBUG=True
)

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

# mostra l'elenco dei lotti
@app.route('/')
def home():
    logged_in = 'user_id' in session
    return render_template('home.html', logged_in=logged_in)

# Restituisce i dati dei lotti disponibili in formato Json
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

@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    if 'user_id' not in session:
        return jsonify({'error': 'Non autorizzato'}), 401
    
    prenotazioni = Prenotazione.query.filter_by(user_id=session['user_id']).all()
    prenotazioni_data = [prenotazione.to_dict() for prenotazione in prenotazioni]
    return jsonify(prenotazioni_data)

@app.route('/lotto/<int:lotto_id>', methods=['GET', 'POST'])
def mostra_lotto(lotto_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # ottengo il record del lotto a partire dal suo ID
    lotto = db.session.get(Lotto, lotto_id)
    if not lotto:
        return 'Lotto non trovato', 404 # codice della risposta di errore in console
    
    # user = db.session.get(User. session{'user.id'})
    # prenotazioni = user.rel_prenotazioni
    prenot_utente = Prenotazione.query.filter_by(
        user_id=session['user_id'],
        lotto_id=lotto_id
        )
    # se esiste già una prenotazione per il lotto dell'utente loggato
    if prenot_utente:
        return render_template('lotto.html', lotto=lotto, prenotazione=prenot_utente)
    
    # se non esiste una prenotazione per il lotto dell'utente loggato
    else:
        return render_template('lotto.html', lotto=lotto, prenotazione=None)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash(f'Benvenuto, {user.nome}!', 'success')
            return redirect(url_for('home'))
        flash('Credenziali non valide', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout effettuato con successo', 'success')
    return redirect(url_for('home'))

@app.route('/registrazione', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        telefono = request.form['telefono']
        email = request.form['email']
        password = request.form['password']
        
        # Verifica se l'email esiste già
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email già registrata. Utilizza un\'altra email.', 'danger')
            return render_template('registrazione.html')
        
        new_user = User(nome=nome, cognome=cognome, telefono=telefono, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrazione effettuata con successo. Puoi effettuare il login.', 'success')
        return redirect(url_for('login'))
    return render_template('registrazione.html')

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)