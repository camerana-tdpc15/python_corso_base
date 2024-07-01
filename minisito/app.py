from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def prima_pagina():

    return render_template ('home.html')

@app.route("/prova")
def seconda_pagina():

    print('ciao')

    var_locale = 'Simone'
    lista = [1,2,3,4,5]

    return render_template ('pagina1.html', var1=var_locale, var2=lista)




app.run(debug=True)