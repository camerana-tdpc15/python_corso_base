from flask import Flask
from markupsafe import escape

app = Flask(__name__) # oggetto applicazione (app)

@app.route("/pippo")  # Lo slash indica la root del sito
def hello_world(): # funzione
    return "<p>Hello, Pippo!</p>"

@app.route("/<name>") # quello che scrive l'utente dopo lo slash viene messo dentro name
def hello(name):
    return f"Hello, {escape(name)}!" # escape controlla che non ci sia codice js o altro, per sicurezza

app.run(debug=True)  # , port=6969)