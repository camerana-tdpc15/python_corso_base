from flask import Flask
from markupsafe import escape

# Creiamo l'oggetto dell'applicazione Flask usando la classe Flask
app = Flask(__name__)

@app.route("/")  # Lo slash indica la root del sito
def hello_world():
    return  'Hello, Pippo!"'

@app.route('/index')  # Un path personalizzato
def index():
    return 'Index Page'

@app.route('/hello')  # Un altro path personalizzato
def hello():
    return 'Hello, World'

# La sintassi <...> permette di leggere una stringa dall'URL
@app.route("/saluta/<name>")  # dopo /saluta/ accetta una qualunque stringa
def hello_name(name):
    return f"Hello, {escape(name)}!"  # Come buona prassi facciamo l'escape, dato
                                      # che è un dato che arriva dall'esterno

# Perché se non facciamo l'escape, un utente potrebbe scrivere ad es. questo:
# http://127.0.0.1:5000/saluta_no_escape/Pluto<h1>Titolo o altro tag
# e ciò inietterebbe un tag HTML.
@app.route("/saluta_no_escape/<name>")
def hello_name_not_escaped(name):
    return f"Hello, {name}!"

# La sintassi <int:...> permette di leggere un numero integer dall'URL
@app.route('/post/<int:post_id>')
def show_post(post_id):
    print(type(post_id))  # Vediamo che il numero è stato converito in int direttamente
    return f'Il post richiesto è {post_id} che è di tipo {escape(type(post_id))}'

# Per leggere percorsi complessi, che contengono più "/"
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # Ora abbiamo ciò che l'utente ha scritto dopo /path/
    print(subpath.split('/'))  # Possiamo ottenere la lista delle "cartelle"
    return f'Il subpath è: {escape(subpath)}'  # Anche qua, come buona prassi facciamo
                                               # l'escape, dato che è un dato che
                                               # arriva dall'esterno

# Questo caso è più insidioso perché un attaccante potrebbe anche iniettare
# del codice Javascript, come ad es:
# http://127.0.0.1:5000/path_no_escape/<script>alert("Hacked!")</script>
# oppure:
# http://127.0.0.1:5000/path_no_escape/%3Cscript%3Ealert(%22Hacked!%22)%3C/script%3E
@app.route('/path_no_escape/<path:subpath>')
def show_subpath_not_escaped(subpath):
    return f'Il subpath è: {subpath}'


# Avviamo il server direttamente
app.run(debug=True)  # , port=6969)