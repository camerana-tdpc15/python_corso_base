import os
from flask import Flask, request, render_template



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

HOME = os.path.join(BASE_DIR, "templates", "home.html")

app = Flask(__name__)



@app.route("/")  # Lo slash indica la root del sito
def render_home():
    return  render_template('home.html')

@app.route('/api/guestbook', methods=['GET', 'POST'])
def guestbook():
    
   
    if request.method == 'POST':
        data = request.json

        print(data)



        # Lettura di nome e messaggio dalla request
    

        nome = data['nome']
        messaggio = data['messaggio']

        print(nome)
        print(messaggio)

        
    else:
       data = request.form
       print(data)
        


app.run(debug=True) 