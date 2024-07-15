import locale
from flask import Flask, flash, render_template, jsonify, request, session, redirect, url_for
from models import db, init_db, prenotazione, utente, replica, evento, locale
from settings import DATABASE_PATH





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # ATTENZIONE: Possiamo usare la password come parametro di ricerca
        #             perché l'abbiamo memorizzata in chiaro (e non come "hash")
        user = utente.query.filter_by(email=email, password=password).first()
        if user:
            session['utente_id'] = user.id
            # flash('Login riuscito!')
            return redirect(url_for('home'))
        else:
            # flash('Credenziali non valide!')
            return redirect(url_for('login'))
    
    elif request.method == 'GET':
        return render_template('login.html')
    




@app.route('/logout')
def logout():
    session.pop('utente_id', None)
    # flash('Logout effettuato con successo!')
    return redirect(url_for('home'))












if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

