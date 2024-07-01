from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def prima_pagina():

    return render_template ('home.html')




@app.route("/prova")
def seconda_pagina():

    return render_template ('pagina1.html')

app.run(debug=True)