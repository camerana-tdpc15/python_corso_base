import locale
from flask import Flask, flash, render_template, jsonify, request, session, redirect, url_for
from models import db, init_db, Evento, Locale, Prenotazione, Replica, Utente
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'


db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask


# Mostra l'elenco dei lotti disponibili
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prenotazioni')
def mostra_prenotazioni():
    return render_template('prenotazioni.html')


# Restituisce i dati dei lotti disponibili in formato JSON
@app.route('/api/eventi', methods=['GET'])
def get_lotti():

    # Leggo i parametri passati in query string
    order = request.args.get('order', 'asc')

    if order == 'asc':
        eventi = Evento.query.order_by(Evento.nome_evento).all()  # -> list es. [<Lotto 1>, <Lotto 2>, ...]
    elif order == 'desc':
        eventi = Evento.query.order_by(Evento.nome_evento.desc()).all()
    else:
        return 'Parametro order non valido. Utilizzare "asc" o "desc".'

    eventi_data = []
    for evento in eventi:
        dict_lotto = evento.to_dict()
        eventi_data.append(dict_lotto)

    return jsonify(eventi_data)


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
        return redirect(url_for("home"))
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
            return redirect(url_for('home'))
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