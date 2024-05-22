from flask import Flask

app = Flask(__name__)



@app.route("/")   #lo slash indica la root cioè la cartella principale
def hello_world():
    return "<p>Hello, World!</p>"

app.run(debug = True)