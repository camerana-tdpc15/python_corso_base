import os
from flask import Flask, render_template, request, session, redirect, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR_PATH, 'db.sqlite3')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognome = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    telefono = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    # messaggi = db.relationship('Messaggio', backref=db.backref('utente'))
    # --- OR ---
    messaggi = db.relationship('Messaggio', back_populates='utente')

class Produttore(db.Model):
    __tablename__ = 'produttore'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produttore = db.Column(db.String(100), unique=True, nullable=False)
    descrizione = db.Column(db.Text, unique=True, nullable=False)
    indirizzo = db.Column(db.Text, unique=True, nullable=False)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    # messaggi = db.relationship('Messaggio', backref=db.backref('utente'))
    # --- OR ---
    messaggi = db.relationship('Messaggio', back_populates='utente')

class Prodotto(db.Model):
    __tablename__ = 'prodotto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    produttore_id = db.Column(db.Integer, db.ForeignKey('produttore.id'),unique=True, nullable=False)
    nome_prodotto = db.Column(db.String(50), unique=True, nullable=False)
    # messaggi = db.relationship('Messaggio', backref=db.backref('utente'))
    # --- OR ---
    messaggi = db.relationship('Messaggio', back_populates='utente')

class Lotto(db.Model):
    __tablename__ = 'lotto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotto.id'), unique=True, nullable=False)
    data_consegna = db.Column(db.DateTime, unique=True, nullable=False)
    qta_unita_misura = db.Column(db.String(10), unique=True, nullable=False)
    qta_lotto = db.Column(db.Integer, unique=True, nullable=False)
    prezzo_unitario = db.Column(db.Float, nullable=False)
    sospeso = db.Column(db.Bit, nullable=False)
    # messaggi = db.relationship('Messaggio', backref=db.backref('utente'))
    # --- OR ---
    messaggi = db.relationship('Messaggio', back_populates='utente')

class Prenotazione(db.Model):
    __tablename__ = 'prenotazione'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utente_id = db.Column(db.Integer, db.ForeignKey('user.id'),unique=True, nullable=False)
    lotto_id = db.Column(db.Integer, db.ForeignKey('lotto.id'),unique=True, nullable=False)
    qta = db.Column(db.Integer, unique=True, nullable=False)
    # messaggi = db.relationship('Messaggio', backref=db.backref('utente'))
    # --- OR ---
    messaggi = db.relationship('Messaggio', back_populates='utente')




@app.route('/')
def home():
    if 'user_id' in session:
        user = db.session.query(Utente).get(session['user_id'])
        return render_template('home.html', utente=user)
    return render_template('home.html')


@app.route('/guestbook')
def guestbook():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('guestbook.html')

@app.route('/api/guestbook', methods=['GET', 'POST'])
def api_guestbook():
    if 'user_id' not in session:
        return jsonify({'error': 'Accesso non autorizzato.'}), 401

    if request.method == 'POST':
        messaggio = request.json.get('messaggio')
        if not messaggio:
            return jsonify({'error': 'Il messaggio non può essere vuoto!'}), 400
        new_message = Messaggio(user_id=session['user_id'], messaggio=escape(messaggio))
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'success': True}), 201

    else:
        messaggi = Messaggio.query.order_by(Messaggio.timestamp.desc()).all()
        response = [
            {'nickname': messaggio.utente.nickname, 'messaggio': messaggio.messaggio} 
            # utente = db.session.get(User, messaggio.user_id)
            # utente.nickname
            for messaggio in messaggi
        ]
        return jsonify(response), 200



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        username = request.form.get('username')
        password = request.form.get('password')
        if not nickname or not username or not password:
            flash('Tutti i campi sono obbligatori!', 'danger')
            return redirect(url_for('signup'))
        if Utente.query.filter_by(username=username).first() or Utente.query.filter_by(nickname=nickname).first():
            flash("Il nickname o l'username sono già in uso!", 'danger')
            return redirect(url_for('signup'))
        new_user = Utente(nickname=nickname, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrazione effettuata con successo!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Utente.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            flash('Login avvenuto correttamente!', 'success')
            return redirect(url_for('guestbook'))
        else:
            flash('Username o password non validi.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout effettuato correttamente.', 'warning')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
