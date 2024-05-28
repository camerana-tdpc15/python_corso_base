from flask import Flask, request, render_template
from markupsafe import escape

# Creiamo l'oggetto dell'applicazione Flask usando la classe Flask
app = Flask(__name__)


# L'URL della home:
# http://127.0.0.1:5000/
@app.route("/")  # Lo slash indica la root del sito
def hello_world():
    return  'Hello, Pippo!'


# La sintassi <int:...> permette di leggere un numero integer dall'URL
# La richiesta potrebbe essere come questa:
# http://127.0.0.1:5000/post/3456
@app.route('/post/<int:post_id>')
def show_post(post_id):
    print(type(post_id))  # Vediamo che il numero è stato converito in int direttamente
    return f"Il post richiesto ha ID {post_id} e l'ID è di tipo {escape(type(post_id))}"


# Metodo che legge eventuali parametri dalla richiesta GET
# La richiesta potrebbe essere come questa:
# http://127.0.0.1:5000/saluta?name=Mario&surname=Rossi
@app.route('/saluta')  # Sottinteso GET
def saluta():
    # Stampa 
    name = request.args.get('name', default='NON DEFINITO')  # Uso un default personalizzato
    surname = request.args.get('surname', default='NON DEFINITO')
    
    # Posso stampare per vedere il contenuto nel log del terminale
    print('name:', name)
    print('surname:', surname)
    
    # Restituisco al client una stringa di saluto con i valori letti dai parametri GET
    return f'Ciao, {name} {surname}!'


# Metodo che legge una variabile dal path e la usa per renderizzare un template
# La richiesta potrebbe essere come questa:
# http://127.0.0.1:5000/hello/
# http://127.0.0.1:5000/hello/Mario
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# Avviamo il server direttamente
app.run(debug=True)