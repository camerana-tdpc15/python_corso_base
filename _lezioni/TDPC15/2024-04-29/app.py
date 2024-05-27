from flask import Flask

app = Flask(__name__)

@app.route("/")  # Lo slash indica la root del sito
def hello_world():
    return "<p>Hello, World!</p>"

app.run(debug=True)  # , port=6969)