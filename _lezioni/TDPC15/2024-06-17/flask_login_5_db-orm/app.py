from flask import Flask, request, render_template, redirect, url_for, session, flash
from settings import DATABASE
from models import init_db, db, User, Film

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE,  # Il path al database
    DEBUG=True  # Imposto qua la modalità debug
                # Vedi app.run() alla fine del file
)

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ottengo l'username e la password inviate tramite FormData
        rx_username = request.form.get('tx_user')
        rx_password = request.form.get('tx_password')

        # NOVITA': Uso il metodo .filter_by() per cercare l'utente dal database
        user = User.query.filter_by(login=rx_username).first()

        # NOVITA': Se l'utente esiste e la password è corretta,
        # imposto la sessione e reindirizzo alla pagina dei film
        if user and user.password == rx_password:
            session['username'] = rx_username
            flash('Login avvenuto correttamente!', 'success')        
            app.logger.info(f"L'utente {rx_username} ha effettuato l'accesso.")
            return redirect(url_for('films'))
        
        # Altrimenti, mostro un messaggio di errore
        else:
            flash('Username o password non validi.', 'danger')
            # NOVITA': Loggo il tentativo di accesso fallito
            app.logger.warning(f"Tentativo di accesso fallito per l'utente {rx_username}.")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logout effettuato correttamente.', 'warning')
    return redirect(url_for('home'))


@app.route('/films')
def films():
    # Se l'utente è autenticato, mostra la pagina dei film
    if 'username' in session:
        films = Film.query.all()
        return render_template('films.html', films=films)
    # Altrimenti riporta sulla pagina di login
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run()  # Notate che ho rimosso il parametro `debug=True` perché ora è
               # impostato in `app.config`. Questo perché altriment la funzione
               # init_db si ritroverebbe il livello di logging non impostato (0).
