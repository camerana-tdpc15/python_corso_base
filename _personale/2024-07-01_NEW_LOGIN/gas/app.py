import locale
from flask import Flask, render_template, jsonify, request, session, redirect, flash, url_for
from models import db, init_db, Lotto, Prodotto, Produttore
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
            return redirect(url_for("lotti_disponibili"))
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
