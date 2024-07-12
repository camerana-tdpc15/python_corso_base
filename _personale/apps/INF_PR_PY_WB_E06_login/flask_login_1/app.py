from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
# Impostiamo una chiave segreta (che vediamo solo noi sviluppatori)
# La chiave servirà per crittografare e firmare i cookies
app.secret_key = 'my_very_secret_key123'

# Struttura dati per contenere gli utenti
# (in futuro leggeremo questi dati direttamente da un database)
USERS = {
    'mrossi': 'osoejfj3',
    'ggangi': 'odoeooeee'
}

# Struttura dati per contenere i film
# (in futuro leggeremo questi dati direttamente da un database)
FILMS = [
    {'title': 'Akira', 'image': 'akira.jpg'},
    {'title': 'Ghost in the Shell', 'image': 'gits.jpg'},
    {'title': 'Blade Runner', 'image': 'blade-runner.jpg'},
    {'title': 'Hackers', 'image': 'hackers.jpg'},
    {'title': 'Nirvana', 'image': 'nirvana.jpg'},
]

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se il metodo è POST:
    if request.method == 'POST':
        # Ottengo l'username e la password inviate tramite FormData
        rx_username = request.form.get('tx_user')
        rx_password = request.form.get('tx_password')

        # Se il nome utente è presente e la password è corretta:
        if rx_username in USERS:
            if rx_password == USERS[rx_username]:

                # Annotiamo nel cookie "session" dell'utente, il fatto che ha
                # effettuato il login.
                session['username'] = rx_username

                # Reindirizziamo alla pagina film usando il nome della
                # funzione di view (endpoint)
                return redirect(url_for('films'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/films')
def films():
    if 'username' in session:
        # Passiamo l'oggetto globale FILMS
        return render_template('films.html', films=FILMS)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)