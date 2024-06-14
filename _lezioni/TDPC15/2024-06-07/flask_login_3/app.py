from flask import Flask, request, render_template, redirect, url_for, session, flash
from db import USERS, FILMS

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

        # Se il nome utente è presente e la password è corretta:
        if rx_username in USERS and rx_password == USERS[rx_username]:
            session['username'] = rx_username
            flash('Login avvenuto correttamente!', 'success')
            return redirect(url_for('films'))
        
        # Altrimenti, se le credenziali non sono corrette:
        else:
            flash('Username o password non validi.', 'danger')

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
        return render_template('films.html', films=FILMS)
    # Altrimenti riporta sulla pagina di login
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
