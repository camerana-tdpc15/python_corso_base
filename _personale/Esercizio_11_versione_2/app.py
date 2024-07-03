from flask import Flask, request, render_template, redirect, url_for, session, flash
from settings import DATABASE
from models import init_db, db, User, Prodotto, Produttore, Lotto, Prenotazione

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
        lotto_disponibile = Lotto.query.filter_by(prodotto_id=prodotto.id, sospeso='False').first()
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/prodotto/<int:prodotto_id>', methods=['GET', 'POST'])
def prodotto(prodotto_id):
    prodotto = Prodotto.query.get(prodotto_id)
    if request.method == 'POST':
        if 'logged_in' in session:
            quantita = int(request.form['quantita'])
            utente_id = session['user_id']
            lotto = Lotto.query.filter_by(prodotto_id=prodotto_id, sospeso='False').first()
            print(f"Quantità richiesta: {quantita}")
            print(f"Lotto trovato: {lotto}")
            if lotto:
                print(f"Quantità lotto disponibile: {lotto.qta_lotto}")
                if lotto.qta_lotto >= quantita:
                    lotto.qta_lotto -= quantita
                    new_prenotazione = Prenotazione(lotto_id=lotto.id, utente_id=utente_id, qta=quantita)
                    db.session.add(new_prenotazione)
                    db.session.commit()
                    flash('Prenotazione effettuata con successo', 'success')
                    return redirect(url_for('carrello'))
                else:
                    print("Quantità non disponibile")
            else:
                print("Lotto non disponibile o sospeso")
            flash('Quantità non disponibile o lotto sospeso', 'danger')
        else:
            return redirect(url_for('login'))
    return render_template('prodotti.html', prodotto=prodotto)

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

        totale = sum(p.qta * p.lotto.prezzo_unitario for p in prenotazioni)

        return render_template('carrello.html', prenotazioni=prenotazioni, totale=totale)
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)

