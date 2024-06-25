from flask import Flask, request, render_template, jsonify,redirect
import os

app = Flask(__name__)

# Ottiene il percorso assoluto della directory del file app.py
BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

# Definisce il percorso completo del file guestbook.txt riprendendo quello di app.py
GUESTBOOK_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.txt')


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
        # Lettura di nome e messaggio dalla request tramite file json
        nome = request.json.get('nome')
        messaggio = request.json.get('messaggio')

        if not nome or not messaggio:
            response = {'error': 'Nome e messaggio sono obbligatori!'}
        else:
            # SCRITTURA SU FILE
            # Apertura del file in modalità append
                with open(GUESTBOOK_PATH, mode='a', encoding='utf-8') as file:
                    # Scrittura del messaggio sul file
                    file.write(f'{nome} : {messaggio}\n')          
                response = {'success': 'ok'}
        return jsonify(response)
    
    # Se la richiesta è GET, dovremmo restituire i messaggi presenti sul file
    else:
        # LETTURA DEL FILE
        # Apertura del file in modalità lettura
        with open(GUESTBOOK_PATH, mode='r', encoding='utf-8') as file:
            # Lettura delle righe del file come lista
            messaggi = file.readlines()# Controllo del file: se il file esiste
            
            
            # Inversione dell'ordine delle righe nella lista
            messaggi.reverse()
            
        
    
        
    # Restituzione delle righe del file in formato JSON
    # trasformo i messaggi in json
    messaggi_json = jsonify(messaggi)

    return messaggi_json

# Avvia l'applicazione Flask in modalità debug
if __name__ == '__main__':
    app.run(debug=True)