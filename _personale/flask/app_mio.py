from flask import Flask
from markupsafe import escape

app = Flask(__name__)       #Flask e una classe
print (__name__)            #lo slash indica la Root---il sito principale
#@app.route("/")
@app.route("/pippo")
def hello_world():
    return "<p>Hello, World, of pippo!</p>"


# app.run(debug=True)

#_________________________________________________________________________________


#from markupsafe import escape

@app.route("/<name>")  #    decoratore
def hello_name(name):
    return f"Hello, {escape(name)}!"   #    senza escape funziona lostesso, escape pulisce il codice


#_________________________________________________________________________________

@app.route('/index')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, Pippo'

#__________________________________________________________________________________


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')    #qui deve essere inserito un integer
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')  #indica un sottopercorso
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


app.run(debug=True)