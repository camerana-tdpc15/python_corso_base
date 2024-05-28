from datetime import date, timedelta
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    esercizi_list = [
        ('Esercizio 1', '/range_numeri'),
        ('Esercizio 2', '/potenze'),
        ('Esercizio 3', '/date')
    ]
    return render_template('index.html', esercizi=esercizi_list)


@app.route('/range_numeri')
def range_numeri():

    start = int(request.args.get('start', default=0))
    stop = int(request.args.get('stop', default=10))

    numeri = range(start, stop)

    return render_template('esercizio1.html', inizio=start, fine=stop, intervallo=numeri)


@app.route('/potenze')
def esercizio_potenze():
    numero = int(request.args.get('base_number', default=2))
    # print('numero ricevuto:', numero)
    potenze = {}
    for esponente in range(2, 6):
        potenze[esponente] = numero ** esponente
    
    print(potenze[esponente])
    
    # fare con dict comprehension


    return render_template('esercizio2_boot.html', powers=potenze, submitted_number=numero)
    

@app.route('/date')
def esercizio_date():
    lista_date = []
    oggi = date.today()
    for num in range(6):
        data = oggi + timedelta(days=2*num)
        lista_date.append(data.strftime('%A %d/%m/%Y'))
    print(lista_date)

    return render_template('esercizio3.html', lista_date=lista_date)


app.run(debug=True)



