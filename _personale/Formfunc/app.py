from flask import Flask, render_template, request, jsonify # importia tutto lo necesario per lavorare
import os

BASE_DIR_PATH = os.path.abspath(os.path.dirname(__name__)) #facciamo un percorso assoluto per il nostro archivo
GUESTBOOK_FILE = 'guestbook.txt' #creamo una variabile  per il nostro .txt
GUESTBOOK_FILE_PATH = os.path.join(BASE_DIR_PATH, GUESTBOOK_FILE)  #uniamo i nostyri path

app = Flask(__name__) #inizializziamo la app

def leggi_guestbook():  #creamo la funzione per leggere il guestbook 
    if not os.path.exists(GUESTBOOK_FILE_PATH): # se non esiste la variabile dove si trova il .txt
        return {} # se non esiste ritorna un diccionario vuoto
    with open(GUESTBOOK_FILE_PATH, 'r') as file:  # apriamo il .txt in modalita lettura
        lines = file.readlines()  # creamo la variabile lines  y questa fa leggere riga per riga dell nosotro file
    messaggi = {} # se cera la variabile messaggi e diciamo che
    for line in lines:  # per ogni riga in rigas
        key, value = line.strip().split(':', 1) # qua togliamo gli spazi con ,strip e con split dividiamo chiave di valore con ':'
        messaggi[key] = value #la chiave del messaggi deve corrispondere al suo valore
    return messaggi 

def vedi_guestbook(nome, messaggio):  # creamo la funzione vedi il guestbook con nome e messaggio come parametri
    with open(GUESTBOOK_FILE_PATH, 'a') as file:#appriamo la unione dei percorsi e in modalita  append, come un file
        file.write(f"{nome}:{messaggio}\n") # scriviamo (appendiamo) nel nostro file il nome-messaggio nella nostra pagina

@app.route('/')  # scriviamo il percoro iniziale
def guestbook():
    return render_template('home.html')

@app.route('/api/guestbook', methods=["GET", "POST"])   # scriviamo il percorso dove ricevera i dati del form e ritornera i messaggi
def api_guestbook():
    if request.method == 'POST':  # controlliamo se il metodo e post
        nome = request.form.get('nome') # otteniamo nome dal form con id nome
        messaggio = request.form.get('messaggio')# otteniamo messaggio dal form con id messaggio

        if not nome or not messaggio:    # facciamo un controllo di errori
            response = {'error': 'Nome e messaggio sono obbligatori'}
            return jsonify(response), 400
        
        vedi_guestbook(nome, messaggio) # se non ci sono errori chiamiamo la funzione e li diamo i parametri

        response = {'success': 'Messaggio aggiunto con successo!'} #e li diamo un messaggio che tutto e andato a buon fine
        return jsonify(response), 200

    elif request.method == 'GET':  # oppure se  il metod e GET 
        messaggi = leggi_guestbook() # creamo la variabile mesasggi dichiarandola con la funzione per leggere i messaggi  
        return jsonify(messaggi), 200 #dove memorizziamo i messaggi nella nostra variabile

if __name__ == '__main__': # inizializziamo la app in modo debug
    app.run(debug=True)