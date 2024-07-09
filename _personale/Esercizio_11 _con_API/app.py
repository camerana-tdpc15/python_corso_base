import locale
import hashlib
from flask import Flask, flash, redirect, render_template, jsonify, request, session, url_for
from models import Prenotazione, User, db, init_db, Lotto, Prodotto, Produttore
from settings import DATABASE

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE,
    DEBUG=True
)

db.init_app(app)

@app.route('/')
def home():
    logged_in = 'user_id' in session
    return render_template('home.html', logged_in=logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/api/lotti', methods=['GET'])
def api_lotti():
    lotti = Lotto.query.all()
    result = []
    for lotto in lotti:
        prenotato = db.session.query(db.func.sum(Prenotazione.qta)).filter_by(lotto_id=lotto.id).scalar() or 0
        disponibile = lotto.qta_lotto - prenotato
        if disponibile > 0 and not lotto.sospeso:
            result.append({
                'id': lotto.id,
                'prodotto': lotto.prodotto_id,
                'data_consegna': lotto.data_consegna.strftime('%Y-%m-%d'),
                'qta_disponibile': disponibile,
                'prezzo_unitario': lotto.prezzo_unitario
            })
    return jsonify(result)

@app.route('/lotti')
def lotti():
    return render_template('lotti.html')

@app.route('/api/prenotazioni', methods=['GET'])
def api_prenotazioni():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    prenotazioni = Prenotazione.query.filter_by(utente_id=user_id).all()
    result = []
    for prenotazione in prenotazioni:
        lotto = Lotto.query.get(prenotazione.lotto_id)
        result.append({
            'id': prenotazione.id,
            'lotto_id': prenotazione.lotto_id,
            'prodotto_id': lotto.prodotto_id,
            'data_consegna': lotto.data_consegna.strftime('%Y-%m-%d'),
            'qta': prenotazione.qta,
            'prezzo_unitario': lotto.prezzo_unitario
        })
    return jsonify(result)

@app.route('/prenotazioni')
def prenotazioni():
    return render_template('prenotazioni.html')

@app.route('/prenotazione/<int:lotto_id>', methods=['GET', 'POST'])
def prenotazione(lotto_id):
    if request.method == 'POST':
        user_id = session.get('user_id')
        qta = request.form['qta']
        lotto = Lotto.query.get(lotto_id)
        
        if not lotto or lotto.sospeso:
            flash('Lotto non disponibile', 'danger')
            return redirect(url_for('lotti'))
        
        prenotato = db.session.query(db.func.sum(Prenotazione.qta)).filter_by(lotto_id=lotto_id).scalar() or 0
        disponibile = lotto.qta_lotto - prenotato

        if int(qta) > disponibile:
            flash('Quantità richiesta superiore a quella disponibile', 'danger')
            return redirect(url_for('lotti'))

        if Prenotazione.query.filter_by(utente_id=user_id, lotto_id=lotto_id).first():
            flash('Hai già prenotato questo lotto', 'warning')
            return redirect(url_for('prenotazioni'))

        nuova_prenotazione = Prenotazione(utente_id=user_id, lotto_id=lotto_id, qta=qta)
        db.session.add(nuova_prenotazione)
        db.session.commit()
        
        flash('Prenotazione effettuata con successo', 'success')
        return redirect(url_for('prenotazioni'))
    
    lotto = Lotto.query.get(lotto_id)
    return render_template('prenotazione.html', lotto=lotto)

@app.route('/modifica-prenotazione/<int:prenotazione_id>', methods=['GET', 'POST'])
def modifica_prenotazione(prenotazione_id):
    prenotazione = Prenotazione.query.get(prenotazione_id)
    if request.method == 'POST':
        qta = request.form['qta']
        lotto = Lotto.query.get(prenotazione.lotto_id)
        
        prenotato = db.session.query(db.func.sum(Prenotazione.qta)).filter_by(lotto_id=prenotazione.lotto_id).scalar() or 0
        disponibile = lotto.qta_lotto - prenotato + prenotazione.qta

        if int(qta) > disponibile:
            flash('Quantità richiesta superiore a quella disponibile', 'danger')
            return redirect(url_for('prenotazioni'))
        
        prenotazione.qta = qta
        db.session.commit()
        
        flash('Prenotazione modificata con successo', 'success')
        return redirect(url_for('prenotazioni'))
    
    return render_template('modifica_prenotazione.html', prenotazione=prenotazione)

@app.route('/api/prodotti', methods=['GET'])
def api_prodotti():
    prodotti = Prodotto.query.all()
    result = []
    for prodotto in prodotti:
        prod_dict = prodotto.to_dict()
        prod_dict['nome_produttore'] = prodotto.produttore.nome_produttore
        result.append(prod_dict)
    return jsonify(result)

@app.route('/api/prodotti/<int:prodotto_id>', methods=['GET'])
def api_prodotto(prodotto_id):
    prodotto = Prodotto.query.get(prodotto_id)
    if prodotto:
        return jsonify(prodotto.to_dict())
    return jsonify({'error': 'Prodotto non trovato'}), 404

@app.route('/elimina-prenotazione/<int:prenotazione_id>', methods=['POST'])
def elimina_prenotazione(prenotazione_id):
    prenotazione = Prenotazione.query.get(prenotazione_id)
    db.session.delete(prenotazione)
    db.session.commit()
    flash('Prenotazione eliminata con successo', 'success')
    return redirect(url_for('prenotazioni'))

if __name__ == '__main__':
    app.run()
