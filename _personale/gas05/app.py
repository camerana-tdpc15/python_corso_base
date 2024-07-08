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

@app.route('/')
def home():
    logged_in = 'user_id' in session
    return render_template('home.html', logged_in=logged_in)

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

@app.route('/prenota/<int:lotto_id>', methods=['GET', 'POST'])
def prenota(lotto_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    lotto = Lotto.query.get_or_404(lotto_id)
    
    if request.method == 'POST':
        qta = int(request.form['qta'])
        if qta <= lotto.get_qta_disponibile():
            prenotazione = Prenotazione(lotto_id=lotto_id, user_id=session['user_id'], qta=qta)
            db.session.add(prenotazione)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return render_template('prenota.html', lotto=lotto, error='Quantità non disponibile')
    
    return render_template('prenota.html', lotto=lotto)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)