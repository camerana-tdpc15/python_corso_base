from flask import Flask, flash, render_template, jsonify, request, session, redirect, url_for
from models import db, Locale, Evento, Replica, Utente, Prenotazione
from populates_db import init_db
from settings import DATABASE_PATH


app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,
 
)

db.init_app(app)
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
        user = Utente.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            # flash('Login riuscito!')
            return redirect(url_for('home'))
        else:
            # flash('Credenziali non valide!')
            return redirect(url_for('login'))
    
    elif request.method == 'GET':
        return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    # flash('Logout effettuato con successo!')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)