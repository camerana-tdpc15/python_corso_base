from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    esercizi_list = [
        ('Index', '/range_numeri'),
        ('Esercizio 1', '/range_numeri?start=1&stop=10'),
        ('Esercizio 2', '/potenze')
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


    return render_template('esercizio2.html', powers=potenze, submitted_number=numero)
    


app.run(debug=True)



