from flask import Flask, request, render_template, redirect, url_for, session, flash
import os
# from settings import DATABASE
# from models import init_db, db, User, Film


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        nome = request.form.get('nome')
        messaggio = request.form.get('messaggio')

        # Scrivi i dati nel file
        with open('messaggi_ES09.txt', 'a') as file:
            file.write(f"{nome}, {messaggio}\n")

    # Leggi i dati dal file
    with open('messaggi_ES09.txt', 'r') as file:
        dati = [line.strip() for line in file]

    return render_template('guestbook_ES09.html', dati=dati)

if __name__ == '__main__':
    app.run(debug=True)



