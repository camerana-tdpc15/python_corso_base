import os
from flask import Flask, request, render_template, jsonify, url_for
from markupsafe import escape



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

HOME = os.path.join(BASE_DIR, "templates", "home.html")
DB_FILE_PATH = os.path.join(BASE_DIR, 'guestbook.txt')

app = Flask(__name__)



@app.route("/")  
def render_home():
    return  render_template('home.html')

@app.route('/api/guestbook', methods=['GET', 'POST'])
def guestbook():
    
   
    if request.method == 'POST':
        data = request.json

        # Lettura di nome e messaggio dalla request
        # stama di prova sul terminale di corretta ricezione 
    
        print(data)
        nome = data['nome']
        messaggio = data['messaggio']
        print(nome)
        print(messaggio)

        if not nome or not messaggio:
            response = {'error': 'Nome e messaggio sono obbligatori!'}
        else:
            # SCRITTURA SU FILE: Apertura del file in modalità append
            with open(DB_FILE_PATH, mode='a', encoding='utf-8') as file:
                
                file.write(f'{escape(nome)}: {escape(messaggio)}\n')
            response = {'success': True}

        return jsonify(response)

        
    else:
        if os.path.exists(DB_FILE_PATH):
            with open(DB_FILE_PATH, mode='r', encoding='utf-8') as file:
                message_to_send = file.readlines()

        else:
            message_to_send = ['non ci sono ancora messaggi :_(<br>vuoi essere il primo?']
        
        return jsonify(message_to_send)


                

     
        


app.run(debug=True) 