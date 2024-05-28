from datetime import date, timedelta
import locale
from flask import Flask, request, render_template

locale.setlocale(locale.LC_ALL, 'it_IT')

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
        ('Esercizio 2', '/potenze'),
        ('Esercizio 3', '/date'),
        ('Esercizio 4', '/manipolazione_stringhe')
    ]
    return render_template('index.html', esercizi=esercizi_list)

# esercizio numero 1
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
    #     2. prima di convertire in int, bisogna controllare che sia possibile (try e except).
    
    try:                                                                        # prova a convertire in intero
       start = int(request.args.get('start', default=0))
       stop = int(request.args.get('stop', default=0))
    except ValueError as err:
        return f'Hai inserito un numero non convertibile in intero: {err}'
    except Exception as err:
        # ATTENZIONE: in questo modo potremmo rivelare all'utente delle possibili falle...
        return f'Si è verificato un errore, riprova: {err}'

    # Crea un range da usarsi nella generazione dell'elenco puntato.
    numeri = range(start, stop)

    # Restituiamo il template renderizzato. Per renderizzarlo, passiamo alla
    # funzione di rendering tutti i dati di cui necessita: i numeri di inizio,
    # fine e il range generato  
    return render_template('esercizio1.html', inizio=start, fine=stop, numeri=numeri)

# esercizio numero 2
# Questa route deve risponde a un URL come questo:
# http://127.0.0.1:5000/potenze
# Oppure a un URL come questo, contenente dei parametri:
# http://127.0.0.1:5000/potenze?base_number=4
@app.route('/potenze')
def esercizio_potenze():
    try:                                                                        # prova a convertire in intero
       numero = int(request.args.get('base_number', default=2))
    except ValueError as err:
        return f'Hai inserito un numero non convertibile in intero: {err}'
    except Exception as err:
        # ATTENZIONE: in questo modo potremmo rivelare all'utente delle possibili falle...
        return f'Si è verificato un errore, riprova: {err}'
    #print('Numero ricevuto: ', numero)         #per verificare che funzioni. il messaggio si vede in consolle
    
    potenze = {}
    for esponente in range(2, 6):
        potenze[esponente] = numero ** esponente

    # potenze = {esponente: numero ** esponente for esponente in range(2, 6)}    # sostituisce le 3 righe precedenti
    print(potenze)
    return render_template('esercizio2.html', powers=potenze, submitted_number=numero)

@app.route('/date')
def esercizio_date():
    lista_date = []
    oggi = date.today()
    for num in range(6):
        data = oggi + timedelta(days=2*num)
        lista_date.append(data.strftime('%A %d/%m/%Y').capitalize())
    print(lista_date)

# dobbiamo convertire le date in una stringa
    return render_template('esercizio3.html', lista_date=lista_date)

@app.route('/manipolazione_stringhe')
def esercizio_concatenazione():
    stringa1 = request.args.get('stringa1', default='-')
    stringa2 = request.args.get('stringa2', default='-')

    risultati = {
        'stringa1': stringa1,
        'stringa2': stringa2,
        'concat_1_2': f'{stringa1} {stringa2}',
        'concat_2_1': f'{stringa2} {stringa1}',
        'iniziali': f'{stringa1[0]}. {stringa2[0]}.',
        'stringa1_invert': stringa1[::-1],
        'stringa2_invert': stringa2[::-1]
    }
    #print(risultati)

    return render_template('esercizio4.html', stringa1=stringa1, stringa2=stringa2, risultati=risultati)



# Avvia direttamente l'applicazione in modalità debug.
app.run(debug=True)





