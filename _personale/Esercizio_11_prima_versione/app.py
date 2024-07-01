from flask import Flask, request, render_template, redirect, url_for, session, flash
from settings import DATABASE
from models import init_db, db, User, Prodotto, Produttore, Lotto, Prenotazione

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE,  # Il path al database
    DEBUG=True                                      # Imposto qua la modalità debug     
)

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ottengo l'email e la password inviate tramite FormData
        rx_email = request.form.get('tx_email')
        rx_password = request.form.get('tx_password')

        # Uso il metodo .filter_by() per cercare l'utente dal database
        user = User.query.filter_by(email=rx_email).first()

        # Se l'utente esiste e la password è corretta, imposto la sessione e reindirizzo alla pagina dei film
        if user and user.password == rx_password:
            session['email'] = rx_email
            flash('Login avvenuto correttamente!', 'success')        
            app.logger.info(f"L'utente {rx_email} ha effettuato l'accesso.")
            return redirect(url_for('prodotti'))
        
        # Altrimenti, mostro un messaggio di errore
        else:
            flash('Email o password non validi.', 'danger')
            # NOVITA': Loggo il tentativo di accesso fallito
            app.logger.warning(f"Tentativo di accesso fallito per l'utente {rx_email}.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logout effettuato correttamente.', 'warning')
    return redirect(url_for('home'))

@app.route('/prodotti')
def prodotti():
    # Se l'utente è autenticato, mostra la pagina dei prodotti
    if 'email' in session:
        prodotti = Prodotto.query.all()
        return render_template('prodotti.html', prodotti=prodotti)
    # Altrimenti riporta sulla pagina di login
    else:
        return redirect(url_for('login'))

def lotti(prodotto_id):
    if 'email' in session:
        lotti = Lotto.query.filter_by(prodotto_id=prodotto_id, sospeso=False).all()
        return render_template('lotti.html', lotti=lotti)
    else:
        return redirect(url_for('login'))    

if __name__ == '__main__':
    with app.app_context(): # forse da togliere, è gia in models
        init_db(app)
    app.run()    