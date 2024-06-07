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
@app.route('/')
def home():
    return render_template('home.html')


# route per Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se il metodo è POST
    if request.method == 'POST':
        # Leggiamo il nome utente (rx_username)
        rx_username = request.form.get('tx_user')
        # Leggiamo la password (rx_password)
        rx_password = request.form.get('tx_password')

        # print('User:', rx_username)
        # print('Password:', rx_password)

        # Per copntrollare se un utente è presente
        if rx_username in USERS:
            if rx_password == USERS[rx_username]:
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
    session.pop('username')
    return redirect(url_for('home'))


# route per Films
@app.route('/films')
def films():
    if 'username' in session:

        films = [
            {'title': 'Akira', 'image': '/static/akira.jpg'}
        ]

        return render_template('films.html', films=films)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)