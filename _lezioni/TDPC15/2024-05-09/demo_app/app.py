from flask import Flask, request, render_template
# from markupsafe import escape

# Creiamo l'oggetto dell'applicazione Flask usando la classe Flask
app = Flask(__name__)

@app.route("/")  # Lo slash indica la root del sito
def hello_world():
    return  'Hello, Pippo!'

# @app.route('/hello')  # Sottinteso GET
# def hello():
#     print('name:', request.args.get('name', default='NON DEFINITO'))
#     print('surname:', request.args.get('surname'))
#     return 'Ciao!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# Avviamo il server direttamente
app.run(debug=True)  # , port=6969)