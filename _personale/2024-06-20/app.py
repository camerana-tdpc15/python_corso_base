import os
from flask import Flask, request, render_template, redirect, url_for, jsonify

BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))  
MIO_FILE_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.txt')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('guestbook.html')



@app.route('/api/guestbook', methods=['GET', 'POST'])
def login():
    # Se il metodo è POST
    if request.method == 'POST':
        # Leggiamo il nome utente (rx_username)
        rx_nome = request.json.get('nome')
        # Leggiamo la password (rx_password)
        rx_messaggio = request.json.get('messaggio')

        if not rx_nome or not rx_messaggio:
            response = {'error' : 'nome e messaggio sono obbligatori'}
            return jsonify(response)
        
        # Per copntrollare se un utente è presente
        print(MIO_FILE_PATH)

        with open(MIO_FILE_PATH, mode='a', encoding='utf-8') as file:
            file.write(f'{rx_nome} {rx_messaggio}\n')
        
    else:    
        if os.path.exists(MIO_FILE_PATH):
           
            with open(MIO_FILE_PATH, mode='a', encoding='utf-8') as file:
                file.write(f'{rx_nome} {rx_messaggio}\n')  # <<-- \n !!    

        return redirect(url_for('api/guestbook'))

    return render_template('guestbook.html')
    

    



if __name__ == '__main__':
    app.run(debug=True)