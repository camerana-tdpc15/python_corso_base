from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from models import Utente, Replica, Prenotazione, Evento, Locale, db
from models import init_db
from settings import DATABASE_PATH

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,
    # SQLALCHEMY_TRACK_MODIFICATIONS=False,
    # DEBUG=True
)

db.init_app(app)

# Mostra la pagina che deve elencare i lotti disponibili
@app.route('/')
def home():
    return render_template('index.html')




@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        cognome = request.form.get("cognome")
        nome = request.form.get("nome")
        telefono = request.form.get("telefono")
        email = request.form.get("email")
        password = request.form.get("password")
        if not cognome or not nome or not telefono or not email or not password:
            flash("Tutti i campi sono obbligatori!", "danger")
            return redirect(url_for("signup"))
        if (
            Utente.query.filter_by(nome=nome).first()
            or Utente.query.filter_by(cognome=cognome).first()
            or Utente.query.filter_by(email=email).first()
        ):
            flash("Il nome o il cognome o l'email sono già in uso!", "danger")
            return redirect(url_for("signup"))
        new_user = Utente(cognome=cognome, nome=nome, telefono=telefono, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registrazione effettuata con successo!", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Utente.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            flash(f'Login riuscito. Benvenuto {user.nome}!', 'success')
            return redirect(url_for('prenotazioni'))
        else:
            flash('Login non riuscito. Controlla email e password.', 'danger')

    return render_template('login.html')




@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
