from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Path del file di testo
BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
GUESTBOOK_FILE = os.path.join(BASE_DIR_PATH, 'guestbook.txt')

# Creo automaticamente il file di testo se non esiste
if not os.path.exists(GUESTBOOK_FILE):
    open(GUESTBOOK_FILE, 'w').close()

# Route per la pagina HTML
@app.route('/')
def guestbook():
    return render_template('guestbook.html')

# Route per l'API
@app.route('/api/guestbook', methods=['GET', 'POST'])
def api_guestbook():
    if request.method == 'POST':
        # Aggiungere un nuovo messaggio
        name = request.json.get('name')
        message = request.json.get('message')
        if name and message:
            with open(GUESTBOOK_FILE, 'a') as file:
                # Aggiungo il nome e il messaggio al file
                file.write(f"{name}: {message}\n")               
            # Messaggio di corretto inserimento    
            return jsonify({'status': 'success'}), 200
        else:
            # Messaggio di errore se i dati non sono validi
            return jsonify({'status': 'error', 'message': 'Invalid input'}), 400
    elif request.method == 'GET':
        # Leggere tutti i messaggi
        messages = []
        with open(GUESTBOOK_FILE, 'r') as file:
            lines = file.readlines()
            # elenco i messaggi dall'ultimo inserito
            for line in reversed(lines):
                name, message = line.strip().split(': ', 1)
                messages.append({'name': name, 'message': message})
        return jsonify(messages), 200

if __name__ == '__main__':
    app.run(debug=True)
