from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")  # Lo slash indica la root del sito
def hello_world():
    return  "<p>Hello, Pippo!</p>"

@app.route("/<name>")
def hello_name(name):
    pippo = '<h1>Ciao</h1>'
    return f"Hello, {escape(pippo + name)}!"

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
    print(type(post_id))
    # show the post with the given id, the id is an integer
    return f'Post {post_id}: {escape(type(post_id))}'

# Per leggere percorsi complessi, che contengono più "/"
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    print(subpath.split('/'))
    return f'Subpath {escape(subpath)}'



app.run(debug=True)  # , port=6969)