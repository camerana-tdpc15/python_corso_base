from flask import Flask, request, render_template, jsonify
# import package
import os

BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
MIO_FILE_PATH = os.path.join(BASE_DIR_PATH, 'questbook.txt')


app = Flask(__name__)

# Route che restituisce la pagina (l'unica pagina, in questo caso)
# che è la "view" (vista) della nostra applicazione.
@app.route('/')
def home():
    return render_template('guestbook.html')


# Route per la gestione delle API del guestbook:
#    - Se la richiesta è GET, restituisce i messaggi presenti sul file.
#    - Se la richiesta è POST, riceve un nuovo messaggio da scrivere sul file.
@app.route('/api/guestbook', methods=['GET', 'POST'])
def guestbook():
    
    # Se la richiesta è POST, dovremmo avere ricevuto un messaggio da scrivere
    if request.method == 'POST':
        # Lettura di nome e messaggio dalla request
        nome = request.json.get('nome')
        messaggio = request.json.get('messaggio')

        if not nome or not messaggio:
            response = {'error': 'Nome e messaggio sono obbligatori!'}
        else:
            # SCRITTURA SU FILE
            with open('guestbook.txt', mode ='a', encoding= 'utf-8') as file:  # Apertura del file in modalità append
                file.write(f'{nome}: {messaggio}\n')
                 # Scrittura del messaggio sul file
            response = {'success': 'ok'}
        return jsonify(response)
    
    # Se la richiesta è GET, dovremmo restituire i messaggi presenti sul file
   
    if os.path.exists(MIO_FILE_PATH):  # Controllo del file: se il file esiste
        # LETTURA DEL FILE
        with open(MIO_FILE_PATH, MODE='r', encoding='utf-8') as file:  # Apertura del file in modalità lettura
            messages = file.readlines  # Lettura delle righe del file come lista
            # Inversione dell'ordine delle righe nella lista
    # Se il file non esiste
    else:
        messages = []  # La risposta sarà una lista vuota
    
    # Restituzione delle righe del file in formato JSON
    return jsonify(messages)
if __name__ == '__main__':
    app.run(debug=True)