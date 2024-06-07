from flask import Flask, request, render_template, redirect, url_for
# importiamo i vari moduli
# L’url_for() in Flask è una funzione utilizzata per creare URL dinamici all’interno 
#   i un’applicazione. Questo evita la necessità di modificare gli URL in tutta 
#   l’applicazione quando si verificano cambiamenti (ad esempio, nella radice dell’URL)

app = Flask(__name__)

USERS = {
    'mrossi': 'osoejfj3',
    'ggangi': 'odoeooeee'
}

@app.route('/')
def home():
    return render_template('index_HomePage.html')
