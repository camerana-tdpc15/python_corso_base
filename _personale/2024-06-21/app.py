from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista di utenti autorizzati (sostituisci con i dati reali)
users = {
    "utente1": "password1",
    "utente2": "password2",
    # ... altri utenti
}

# Lista di film (sostituisci con i dati reali)
movies = [
    {
        "title": "Film 1",
        "poster": "film1.jpg"
    },
    {
        "title": "Film 2",
        "poster": "film2.jpg"
    },
    # ... altri film
]

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['tx_user']
        password = request.form['tx_password']

        if username in users and users[username] == password:
            return render_template('movies.html', movies=movies)
        else:
            return render_template('login.html', error="Credenziali errate")
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
