from flask import Flask
from markupsafe import escape

# Creiamo l'oggetto dell'applicazione Flask usando la classe Flask
app = Flask(__name__)

# METODO SICURO
# La sintassi <...> permette di leggere una stringa dall'URL
@app.route("/saluta/<name>")  # dopo /saluta/ accetta una qualunque stringa
def hello_name(name):
    return f"Hello, {escape(name)}!"  # Come buona prassi facciamo l'escape, dato
                                      # che è un dato che arriva dall'esterno

# METODO NON SICURO
# Perché se non facciamo l'escape, un utente potrebbe scrivere ad es. questo:
# http://127.0.0.1:5000/saluta_no_escape/Pluto<h1>Titolo o altro tag
# e ciò inietterebbe un tag HTML.
@app.route("/saluta_no_escape/<name>")
def hello_name_not_escaped(name):
    return f"Hello, {name}!"


# METODO SICURO
# Per leggere percorsi complessi, che contengono più "/", abbiamo il tipo "path"
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # Ora abbiamo ciò che l'utente ha scritto dopo /path/
    print(subpath.split('/'))  # Possiamo ottenere la lista delle "cartelle"
    return f'Il subpath è: {escape(subpath)}'  # Anche qua, come buona prassi facciamo
                                               # l'escape, dato che è un dato che
                                               # arriva dall'esterno

# METODO NON SICURO
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