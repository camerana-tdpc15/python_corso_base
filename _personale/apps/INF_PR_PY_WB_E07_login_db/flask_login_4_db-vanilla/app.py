from flask import Flask, request, render_template, redirect, url_for, session, flash
from db import _init_user_table, get_user_password, FILMS

app = Flask(__name__)

app.secret_key = 'my_very_secret_key123'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ottengo l'username e la password inviate tramite FormData
        rx_username = request.form.get('tx_user')
        rx_password = request.form.get('tx_password')

        # NOVITA': Uso la funzione per leggere la password dell'utente dal database
        db_password = get_user_password(rx_username)

        # Se la password è corretta, imposto la sessione e reindirizzo alla pagina dei film
        if rx_password == db_password:
            session['username'] = rx_username
            flash('Login avvenuto correttamente!', 'success')
        
            # NOVITA': Loggo l'accesso riuscito
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
        # Renderizza la pagina dei film passando l'ogetto FILMS importato da db.py
        return render_template('films.html', films=FILMS)
    # Altrimenti riporta sulla pagina di login
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    
    # Inizializza la tabella degli utenti
    _init_user_table()

    app.run(debug=True)
