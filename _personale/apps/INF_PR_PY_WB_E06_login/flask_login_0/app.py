# NOVITA': Importiamo anche gli oggetti "session", "redirect" e "url_for" !
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

# route per Home
@app.route('/')  # nome ROUTE '/'
def home():      # nome ENDPOINT 'home'
    return render_template('home.html')


# route per Login
@app.route('/login', methods=['GET', 'POST'])  # nome ROUTE '/login'
def login():                                   # nome ENDPOINT 'login'
    # Se il metodo è POST
    if request.method == 'POST':
        # Leggiamo il nome utente (rx_username)
        rx_username = request.form.get('tx_user')
        # Leggiamo la password (rx_password)
        rx_password = request.form.get('tx_password')

        # Controllo se l'utente è presente
        if rx_username in USERS:
            # Controllo se la password è corretta
            if rx_password == USERS[rx_username]:
                
                # Aggiungiamo la chiave 'username' all'oggetto session e impostiamo
                # il nome dell'utente come valore. Questo sarà scritto in un cookie.
                session['username'] = rx_username

                # ATTENZIONE: Notate che se restituite il template films.html
                #             l'URL rimane il medesimo!
                # return render_template('films.html')

                # Bisogna invece fare un redirect:
                return redirect(url_for('films'))
                # Che equivale a sctivere direttamente
                # return redirect('/films')
                # ...ma questa scrittura è meno manutenibile
                # in caso di ridenominazione della route

    return render_template('login.html')


@app.route('/logout')
def logout():
    # Rimuoviamo la chiave 'username' da session, e quindi anche dal cookie
    session.pop('username', None)
    # Reindirizziamo alla home
    return redirect(url_for('home'))


# route per Films
@app.route('/films')
def films():
    # Se la chiave 'username' è presente nell'oggetto session, vuol dire che
    # l'utente ha già effettuato il login, quindi mostriamo la pagina dei film
    if 'username' in session:

        # Struttura dati per contenere i film
        # (in futuro leggeremo questi dati direttamente da un database)
        films = [
            
            # L'immagine la posso indicare direttamente con un path hard-coded.
            {'title': 'Akira', 'image': '/static/akira.jpg'},
            
            # Oppure usando "url_for" che è molto meglio e consigliato.
            {'title': 'Blade Runner', 'image': url_for('static', filename='blade-runner.jpg')},
        ]

        # Infine renderizzo il template passando l'oggetto 'films' come argomento
        return render_template('films.html', films=films)
    # Altrimenti, se l'utente non è autenticato, reindirizziamo sulla pagina di login
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
