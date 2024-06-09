from flask import Flask, request, render_template, send_from_directory

# 1. creazione dell'applicazione Flask
app = Flask(__name__)

# 2. definizione Funzione per calcolare il risultato
# la funzione calcola prende 3 argomenti: number1, number2 e operation
def _calcola(number1, number2, operation):
    # Controlla che i parametri passati siano numeri validi 
    # cercando di convertire i number1 e 2 in float
    try:
        number1 = float(number1)
        number2 = float(number2)
    # nel caso fallisca la conversione da un errore
    except ValueError:
        return 'Errore: Uno o entrambi i numeri inseriti non sono validi.'

    # inizializzazione del risultato
    result = ''
    
    # in base al valore dell'operation la funzione esegue l'operazione corrispondente:
    # addizzione
    if operation == 'add':
        result = number1 + number2
    # sottrazione
    elif operation == 'subtract':
        result = number1 - number2
    # moltiplicazione
    elif operation == 'multiply':
        result = number1 * number2
    # divisione
    elif operation == 'divide':
        if number2 == 0:
            result = 'Errore: Divisione per zero'
        else:
            result = number1 / number2
    # se l'operazione non viene riconosciuta viene restituito un messaggio d'errore
    else:
        result = 'Errore: Operazione non riconosciuta: ' + operation
        
    # ritorna il risultato
    return result


# 3. Route principale
@app.route('/')
# definizione della index che gestisce le richieste alla root url
def index():
    # Crezione della Lista di dizionari contenenti titolo e URL di ogni versione della calcolatrice
    calculators = [
        {'title': 'Calcolatrice JavaScript stand-alone', 'url': '/calculator_js_standalone'},
        {'title': 'Calcolatrice con JavaScript e calcolo lato server', 'url': '/calculator_js_client'},
        {'title': 'Calcolatrice a Template', 'url': '/calculator_template'}
    ]
    # Passiamo la lista al template che genera la pagina web usando il template index.html
    return render_template('index.html', calculators=calculators)


# 4. Route per la calcolatrice stand-alone JavaScript
@app.route('/calculator_js_standalone', methods=['GET'])
def calculator_js_standalone():
    # la funzione send_from_directory è utilizzatat per inviare un fil specifico dal filesystem del server al client
    # in questo caso vien inviato alla directory 'static'
    return send_from_directory('static', 'calculator_js_standalone.html')

# 5. Route per la calcolatrice  con calcolo lato server
@app.route('/calculator_js_client', methods=['GET', 'POST'])
def calculator_js_client():
    # gestione delle richieste POST
    if request.method == 'POST':
        # Se la richiesta è in formato JSON,
        # (form inviato tramite oggetto JSON creato manualmente)
        # i dati vengono ottenuti 'request.get_json()'
        if request.is_json:
            data = request.get_json()
        # Altrimenti, dà per scontato che la richiesta sia in formato "form"
        # (form inviato tramite FormData)
        else:
            # altrimenti i dati vengono ottenuti con 'request.form'
            data = request.form
        # registrazione dei dati ricevuti nei log dell'applicazione    
        app.logger.info('Request form: %s', data)
        
        # elaborazione dell'operazione
        operation = data.get('operation')
        # viene estratta l'operazione dai dati ricevuti  e viene chiamata la funzione '_calcola()'
        result = _calcola(
            data.get('number1'),
            data.get('number2'),
            operation
        )
        # il risultato viene convertito in stringa
        return str(result)
    
    # altrimenti se la richiesta è di tipo GET
    # viene inviato il file HTML al 'calculator_js_client.html' dalla directory 'static'
    else:
        return send_from_directory('static', 'calculator_js_client.html')
    
# 6. Route per la calcolatrice basata sul Template
# specifica che la funzione risponderà sia a richietste GET che POST
@app.route('/calculator_template', methods=['GET', 'POST'])
# definizione della funzione
def calculator_template():
    # definizione del template
    # specifica il template HTML da utilizzare
    TEMPLATE = 'calculator_template.html'
    #TEMPLATE = 'calculator_template_base.html'
    # registra nei LOG i dati ricevuti tramite il form 'request.form' e i parametri della query 'Request args'
    app.logger.info('Request form: %s', request.form)
    app.logger.info('Request args: %s', request.args)
    # inizializzazione della variabile result
    result = ''
    # gestione delle richieste POST
    if request.method == 'POST':
        # viene estratta l'operazione dai dati del form
        operation = request.form.get('operation')
        # viene chiamata la funzione '_calcola' con i numeri e operazione specificata
        # il risultato dell'operazione viene memorizzato in result
        result = _calcola(
            request.form.get('number1'),
            request.form.get('number2'),
            operation
        )

        # renderizza ilo template specificato passando il risultato come variabile al template
    return render_template(TEMPLATE, result=result)


# 7. Avvio dell'applicazione
if __name__ == '__main__':
    app.run(debug=True)
