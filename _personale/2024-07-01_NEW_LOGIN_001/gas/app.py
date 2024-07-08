import locale
from flask import Flask, render_template, jsonify, request, session, redirect, flash, url_for
from models import db, init_db, Lotto, Prodotto, Produttore, User
from settings import DATABASE_PATH

locale.setlocale(locale.LC_TIME, 'it_IT')


app = Flask(__name__)

app.config.update(
    SECRET_KEY="my_very_secret_key123",
    SQLALCHEMY_DATABASE_URI="sqlite:///" + DATABASE_PATH,  # Il path al database
    DEBUG=True,  # Imposto qua la modalità debug
    # Vedi app.run() alla fine del file
)

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/api/lotti', methods=['GET'])
def get_lotti():
    lotti = Lotto.query.all()

    lotti_data = []

    for lotto in lotti:
        prodotto = db.session.get(Prodotto, lotto.prodotto_id)
        produttore = db.session.get(Produttore, prodotto.produttore_id)
        data = {
            'id': lotto.id,
            'data_consegna': lotto.data_consegna,
            'get_date': lotto.get_date(),  # es. "Giovedì 27/06/2024"
            'get_prezzo_str': lotto.get_prezzo_str(),  # es. "8.50 €/L"
            'get_qta_disponibile': lotto.get_qta_disponibile(), # es. 94
            'qta_unita_misura': lotto.qta_unita_misura,
            'qta_lotto': lotto.qta_lotto,
            'prezzo_unitario': lotto.prezzo_unitario,
            'sospeso': lotto.sospeso,
            'prodotto_id': lotto.prodotto_id,
            'prodotto': {
                'nome_prodotto': prodotto.nome_prodotto,
                'produttore': {
                    'nome_produttore': produttore.nome_produttore
                }
            }
        }

        lotti_data.append(data)
    
    return jsonify(lotti_data)


@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    ...


# @TODO: Implementare il login / logout
...





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
            User.query.filter_by(nome=nome).first()
            or User.query.filter_by(cognome=cognome).first()
            or User.query.filter_by(email=email).first()
        ):
            flash("Il nome o il cognome o l'email sono già in uso!", "danger")
            return redirect(url_for("signup"))
        new_user = User(cognome=cognome, nome=nome, telefono=telefono, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registrazione effettuata con successo!", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session["user_id"] = user.id
            flash("Login avvenuto correttamente!", "success")
            return redirect(url_for("home"))
        else:
            flash("Username o password non validi.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logout effettuato correttamente.", "warning")
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
