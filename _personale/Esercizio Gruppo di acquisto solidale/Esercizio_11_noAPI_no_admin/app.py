from flask import Flask, request, render_template, redirect, url_for, session, flash
from settings import DATABASE
from models import init_db, db, User, Prodotto, Produttore, Lotto, Prenotazione
from datetime import datetime

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE,
    DEBUG=True
)

db.init_app(app)

@app.route('/')
def home():
    prodotti = Prodotto.query.all()
    prodotti_disponibili = []
    for prodotto in prodotti:
        lotto_disponibile = Lotto.query.filter_by(prodotto_id=prodotto.id, sospeso=0).first()
        prodotti_disponibili.append((prodotto, lotto_disponibile is not None))
    return render_template('home.html', prodotti_disponibili=prodotti_disponibili)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for('home'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
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


@app.route('/prodotto/<int:prodotto_id>', methods=['GET', 'POST'])
def prodotto(prodotto_id):
    prodotto = Prodotto.query.get(prodotto_id)
    
    # Calcola la quantità disponibile
    lotti = Lotto.query.filter_by(prodotto_id=prodotto_id, sospeso=False).all()
    totale_disponibile = sum(lotto.qta_lotto for lotto in lotti)
    totale_prenotato = sum(prenotazione.qta for prenotazione in Prenotazione.query.join(Lotto).filter(Lotto.prodotto_id == prodotto_id).all())
    quantita_disponibile = max(totale_disponibile - totale_prenotato, 0)

    # Calcola il prezzo del prodotto basato sui lotti disponibili
    prezzi_lotti = [lotto.prezzo_unitario for lotto in lotti]
    prezzo = min(prezzi_lotti) if prezzi_lotti else None

    # Recupera l'unità di misura
    unita_misura = lotti[0].qta_unita_misura if lotti else 'N/A'
    
    if request.method == 'POST':
        if 'logged_in' in session:
            quantita = int(request.form['quantita'])
            utente_id = session['user_id']
            if quantita <= quantita_disponibile:
                # Trova un lotto disponibile per fare la prenotazione
                for lotto in lotti:
                    if lotto.qta_lotto >= quantita:
                        lotto.qta_lotto -= quantita
                        new_prenotazione = Prenotazione(lotto_id=lotto.id, utente_id=utente_id, qta=quantita)
                        db.session.add(new_prenotazione)
                        db.session.commit()
                        flash('Prenotazione effettuata con successo', 'success')
                        return redirect(url_for('carrello'))
                flash('Quantità non disponibile in nessun lotto', 'danger')
            else:
                flash('Quantità non disponibile o lotto sospeso', 'danger')
        else:
            return redirect(url_for('login'))
    return render_template('prodotti.html', prodotto=prodotto, quantita_disponibile=quantita_disponibile, prezzo=prezzo, lotti=lotti, unita_misura=unita_misura)

@app.route('/carrello', methods=['GET', 'POST'])
def carrello():
    if 'logged_in' in session:
        utente_id = session['user_id']
        prenotazioni = Prenotazione.query.filter_by(utente_id=utente_id).all()

        if request.method == 'POST':
            prenotazione_id = request.form['prenotazione_id']
            prenotazione = Prenotazione.query.get(prenotazione_id)
            if prenotazione and prenotazione.utente_id == utente_id:
                if 'update' in request.form:
                    new_quantity = int(request.form['quantita'])
                    diff = new_quantity - prenotazione.qta
                    if prenotazione.lotto.qta_lotto >= diff:
                        prenotazione.lotto.qta_lotto -= diff
                        prenotazione.qta = new_quantity
                        db.session.commit()
                        flash('Quantità aggiornata con successo', 'success')
                    else:
                        flash('Quantità non disponibile', 'danger')
                elif 'delete' in request.form:
                    prenotazione.lotto.qta_lotto += prenotazione.qta
                    db.session.delete(prenotazione)
                    db.session.commit()
                    flash('Prodotto rimosso con successo', 'success')
                return redirect(url_for('carrello'))

        totale = round(sum(p.qta * p.lotto.prezzo_unitario for p in prenotazioni), 2)

        return render_template('carrello.html', prenotazioni=prenotazioni, totale=totale)
    return redirect(url_for('login'))

@app.route('/nuovo_produttore', methods=['GET', 'POST'])
def nuovo_produttore():
    if request.method == 'POST':
        nome_produttore = request.form['nome_produttore']
        descrizione = request.form['descrizione']
        indirizzo = request.form['indirizzo']
        telefono = request.form['telefono']
        email = request.form['email']
        nuovo_produttore = Produttore(nome_produttore=nome_produttore, descrizione=descrizione, indirizzo=indirizzo, telefono=telefono, email=email)
        db.session.add(nuovo_produttore)
        db.session.commit()
        flash('Produttore aggiunto con successo', 'success')
        return redirect(url_for('home'))
    return render_template('nuovo_produttore.html')

@app.route('/nuovo_prodotto', methods=['GET', 'POST'])
def nuovo_prodotto():
    produttori = Produttore.query.all()
    if request.method == 'POST':
        produttore_id = request.form['produttore_id']
        nome_prodotto = request.form['nome_prodotto']
        image_url = request.form['image_url']
        nuovo_prodotto = Prodotto(produttore_id=produttore_id, nome_prodotto=nome_prodotto)
        db.session.add(nuovo_prodotto)
        db.session.commit()
        flash('Prodotto aggiunto con successo', 'success')
        return redirect(url_for('home'))
    return render_template('nuovo_prodotto.html', produttori=produttori)

@app.route('/nuovo_lotto', methods=['GET', 'POST'])
def nuovo_lotto():
    prodotti = Prodotto.query.all()
    if request.method == 'POST':
        prodotto_id = request.form['prodotto_id']
        data_consegna = datetime.strptime(request.form['data_consegna'], '%Y-%m-%d')
        qta_unita_misura = request.form['qta_unita_misura']
        qta_lotto = request.form['qta_lotto']
        prezzo_unitario = request.form['prezzo_unitario']
        sospeso = request.form['sospeso'] == 'true'
        nuovo_lotto = Lotto(prodotto_id=prodotto_id, data_consegna=data_consegna, qta_unita_misura=qta_unita_misura, qta_lotto=qta_lotto, prezzo_unitario=prezzo_unitario, sospeso=sospeso)
        db.session.add(nuovo_lotto)
        db.session.commit()
        flash('Lotto aggiunto con successo', 'success')
        return redirect(url_for('home'))
    return render_template('nuovo_lotto.html', prodotti=prodotti)

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)

