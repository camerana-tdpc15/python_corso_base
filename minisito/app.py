from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def prima_pagina():

    risultato  = ' 2 + 2'
    lista = ["mele", "pere", "cani"]

    return render_template ('home.html',var_2 = risultato, var_3 = lista )




@app.route("/prova")
def seconda_pagina():

    return render_template ('pagina1.html')

app.run(debug=True)