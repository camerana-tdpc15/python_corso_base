import os
from flask import Flask, request, render_template, jsonify, url_for
from markupsafe import escape

BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
GB_FILE_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.txt')

app = Flask(__name__, )

app.secret_key = 'supersecretkey'  # Necessario per i flash messages

# Route che restituisce la pagina (l'unica pagina, in questo caso)
# che è la "view" (vista) della nostra applicazione.
@app.route('/')
def home():
    return render_template('guestbook.html')


# Route per la gestione delle API del guestbook:
#    - Se la richiesta è GET, restituisce i messaggi presenti sul file.
#    - Se la richiesta è POST, riceve un nuovo messaggio da scrivere sul file
#      e poi restituisce un messaggio con l'esito dell'operazione.
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
            # SCRITTURA SU FILE: Apertura del file in modalità append
            with open(GB_FILE_PATH, mode='a', encoding='utf-8') as file:
                # Scrivo una riga al fondo del file nel formato "nome: messaggio"
                # IMPORTANTE: \n alla fine della riga!
                file.write(f'{escape(nome)}: {escape(messaggio)}\n')
            response = {'success': True}
        return jsonify(response)
    
    # Se la richiesta è GET, dovremmo restituire i messaggi presenti sul file
    else:
        # Controllo del file: se il file esiste
        if os.path.exists(GB_FILE_PATH):
            # LETTURA DEL FILE: Apertura del file in modalità lettura
            with open(GB_FILE_PATH, mode='r', encoding='utf-8') as file:
                # Lettura delle righe del file come lista di stringhe
                messages = file.readlines()
            # Ordina i messaggi dal più recente al più vecchio
            messages.reverse()
        # Se il file non esiste
        else:
            messages = []  # La risposta sarà una lista vuota
        
        # Restituzione delle righe del file in formato JSON
        return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)