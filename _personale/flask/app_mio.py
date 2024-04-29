from flask import Flask

app = Flask(__name__)       #Flask e una classe
print (__name__)            #lo slash indica la Root---il sito principale
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


app.run(debug=True)