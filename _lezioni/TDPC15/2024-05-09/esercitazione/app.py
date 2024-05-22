from flask import Flask, request, render_template

app = Flask(__name__)

# Questa route risponde a un questo URL:
# http://127.0.0.1:5000/
# ovvero la root del sito
@app.route('/')
def index():
    # Creo una lista di tuple per creare un elenco di link
    # (testo_link, url_link)
    esercizi_list = [
        ('Esercizio 1', '/range_numeri'),
        ('Esercizio 1 TEST', '/range_numeri?start=1&stop=10')
    ]
    return render_template('index.html', esercizi=esercizi_list)

# Questa route deve risponde a un URL come questo:
# http://127.0.0.1:5000/range_numeri
# Oppure a un URL come questo, contenente dei parametri:
# http://127.0.0.1:5000/range_numeri?start=1&stop=10
@app.route('/range_numeri')
def esercizio_range():

    # Leggiamo gli eventuali parametri passati nell'URL (?start=...&stop=...)
    #     ATTENZIONE - DA SVOLGERE (vedi notebook esercitazione.ipynb):
    #     1. se uno o entrambi i parametri non fossero presenti, è necessario
    #       avere un valore di default.
    #     2. prima di convertire in int, bisogna controllare che sia possibile.
    start = request.args.get('start')
    stop = request.args.get('stop')

    # Crea un range da usarsi nella generazione dell'elenco puntato.
    numeri = range(start, stop)

    # Restituiamo il template renderizzato. Per renderizzarlo, passiamo alla
    # funzione di rendering tutti i dati di cui necessita: i numeri di inizio,
    # fine e il range generato  
    return render_template('esercizio1.html', inizio=start, fine=stop, numeri=numeri)


# Avvia direttament l'applicazione in modalità debug.
app.run(debug=True)
