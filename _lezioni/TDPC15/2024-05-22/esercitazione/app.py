from datetime import date, timedelta 
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
        ('Esercizio 2', '/potenze'),
        ('Esercizio 3', '/date')
    ]
    return render_template('index.html', esercizi=esercizi_list)

# Questa route deve risponde a un URL come questo:
# http://127.0.0.1:5000/range_numeri
# Oppure a un URL come questo, contenente dei parametri:
# http://127.0.0.1:5000/potenze
# http://127.0.0.1:5000/range_numeri

@app.route('/range_numeri')
def esercizio_range():
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
# http://127.0.0.1:5000/potenze?number=4
@app.route('/potenze')
def esercizio_potenze():
    numero = int(request.args.get('base_number', default=2))
    # print('Numero ricevuto:', numero)
    potenze = {}

    for esponente in range(2, 21):
        potenze[esponente] = numero ** esponente

    # potenze = {... dict comprehension}
    print(potenze)
    return render_template('esercizio2.html', powers=potenze, submitted_number=numero)

# http://127.0.0.1:5000/date

@app.route('/date')
def esercizio_date():
    lista_date = []
    oggi = date.today()

    for num in range (6):
        data = oggi + timedelta(days=2*num) 
        lista_date.append(data.strftime('%A %d/%m/%Y'))
    print(lista_date)

    return render_template('esercizio3.html', lista_date=lista_date)

# http://127.0.0.1:5000/manipolazione_stringhe?stringa1=luca&stringa2=paolo

@app.route('/manipolazione_stringhe')
def esercizio_stringhe():
    str1 = (request.args.get('stringa1', default='/'))
    str2 = (request.args.get('stringa2', default=''))

    risultati = {
        'stringa1': str1,
        'stringa2': str2,
        'concat_1_2': str1 + ' ' + str2,
        'concat_2_1': f'{str2} {str1}',
        'iniziali': f'{str1[0]} e {str2[0]}',
        'stringa_invertita': str1[::-1]
    }
    
    return render_template('esercizio4.html', risultati=risultati, stringa1=str1, stringa2=str2)



# Avvia direttamente l'applicazione in modalità debug.
app.run(debug=True)
