from flask import Flask,render_template,request,jsonify
import os


BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
MIO_FILE_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.txt')

app = Flask(__name__)

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
            return jsonify(response)
        else:
         
    
         if os.path.exists(MIO_FILE_PATH):
            # LETTURA DEL FILE
            with open(MIO_FILE_PATH, 'r') as file:
                messages = file.readlines()
                #messages.reverse()
         else:
            messages = []   
        return jsonify(messages)
     
           
     # Se la richiesta è GET, dovremmo restituire i messaggi presenti sul file
    else:
        if  os.path.exists('guestbook.txt'):  # Controllo del file: se il file esiste
        
            # LETTURA DEL FILE
            with open('guestbook.txt','r') as file:  # Apertura del file in modalità lettura
                messages = file.readlines()  # Lettura delle righe del file come lista
                # messages.reverse() # Inversione dell'ordine delle righe nella lista
        # Se il file non esiste
        else:
            messages = []  # La risposta sarà una lista vuota
        
        # Restituzione delle righe del file in formato JSON
        return jsonify(messages)



if __name__ == '__main__':
    app.run(debug=True)
