from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

# Funzione per calcolare il risultato
def _calcola(number1, number2, operation):
    # Controlla che i parametri passati siano numeri validi
    try:
        number1 = float(number1)
        number2 = float(number2)
    except ValueError:
        return 'Errore: Uno o entrambi i numeri inseriti non sono validi.'

    result = ''
    if operation == 'add':
        result = number1 + number2
    elif operation == 'subtract':
        result = number1 - number2
    elif operation == 'multiply':
        result = number1 * number2
    elif operation == 'divide':
        if number2 == 0:
            result = 'Errore: Divisione per zero'
        else:
            result = number1 / number2
    else:
        result = 'Errore: Operazione non riconosciuta: ' + operation
    
    return result


@app.route('/')
def index():
    # Lista di dizionari contenenti titolo e URL di ogni versione della calcolatrice
    calculators = [
        {'title': 'Calcolatrice JavaScript stand-alone', 'url': '/calculator_js_standalone'},
        {'title': 'Calcolatrice con JavaScript e calcolo lato server', 'url': '/calculator_js_client'},
        {'title': 'Calcolatrice a Template', 'url': '/calculator_template'}
    ]
    # Passiamo la lista al template
    return render_template('index.html', calculators=calculators)

@app.route('/calculator_js_standalone', methods=['GET'])
def calculator_js_standalone():
    return send_from_directory('static', 'calculator_js_standalone.html')

@app.route('/calculator_js_client', methods=['GET', 'POST'])
def calculator_js_client():
    if request.method == 'POST':
        # Se la richiesta è in formato JSON,
        # (form inviato tramite oggetto JSON creato manualmente)
        if request.is_json:
            data = request.get_json()
        # Altrimenti, dà per scontato che la richiesta sia in formato "form"
        # (form inviato tramite FormData)
        else:
            data = request.form
        app.logger.info('Request form: %s', data)
        operation = data.get('operation')
        result = _calcola(
            data.get('number1'),
            data.get('number2'),
            operation
        )
        return str(result)
    else:
        return send_from_directory('static', 'calculator_js_client.html')

@app.route('/calculator_template', methods=['GET', 'POST'])
def calculator_template():
    TEMPLATE = 'calculator_template.html'
    # TEMPLATE = 'calculator_template_base.html'
    app.logger.info('Request form: %s', request.form)
    app.logger.info('Request args: %s', request.args)
    result = ''
    if request.method == 'POST':
        operation = request.form.get('operation')
        result = _calcola(
            request.form.get('number1'),
            request.form.get('number2'),
            operation
        )

    return render_template(TEMPLATE, result=result)


if __name__ == '__main__':
    app.run(debug=True)
