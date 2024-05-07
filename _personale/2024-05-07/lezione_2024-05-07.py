from flask import Flask
from markupsafe import escape

app = Flask(__name__) # oggetto applicazione (app)

@app.route("/pippo")  # Lo slash indica la root del sito
def hello_world(): # funzione
    return "<p>Hello, Pippo!</p>"

@app.route("/<name>") # quello che scrive l'utente dopo lo slash viene messo dentro name
def hello_name(name):
    return f"Hello, {escape(name)}!" # escape controlla che non ci sia codice js o altro, per sicurezza

@app.route('/index')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

app.run(debug=True)  # questo deve essere sempre al fondo! Il debug va disattivato quando pubblichiamo il sito