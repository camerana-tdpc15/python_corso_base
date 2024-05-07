from flask import Flask  

app = Flask(__name__)
print(repr(__name__))

@app.route("/") # lo slash indica la root
def hello_world():
    return "<p>Hello, World!</p>"
app.run(debug=True)
