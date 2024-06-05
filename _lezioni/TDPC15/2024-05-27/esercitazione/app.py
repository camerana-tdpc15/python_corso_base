from datetime import date, timedelta
from flask import Flask, request, render_template

import locale

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)

@app.route('/login')
def esercizio_login():
    try:
        start = int(request.args.get('start', default=0))
        stop = int(request.args.get('stop', default=0))
    except ValueError as err:
        return f'Hai inserito un numero non convertibile in intero: {err}'
    except Exception as err:
        # ATTENZIONE: In questo modo potremmo rivelare all'utente delle possibili falle...
        return f'Si è verificato un errore. Riprova: {err}'
    
    # Crea un range da usarsi nella generazione dell'elenco puntato.
    numeri = range(start, stop)

    # Restituiamo il template renderizzato. Per renderizzarlo, passiamo alla
    # funzione di rendering tutti i dati di cui necessita: i numeri di inizio,
    # fine e il range generato  
    return render_template('esercizio1.html', inizio=start, fine=stop, numeri=numeri)

# Questa route deve risponde a un URL come questo:
# http://127.0.0.1:5000/potenze
# Oppure a un URL come questo, contenente dei parametri:
# http://127.0.0.1:5000/potenze?base_number=4





# Avvia direttamente l'applicazione, in modalità debug.
app.run(debug=True)
