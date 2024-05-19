from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    esercizi_list = [
        ('Esercizio 1', '/range_numeri'),
        ('Esercizio 2', '/range_numeri?start=1&stop=10')
    ]

    return render_template('index.html', esercizi=esercizi_list)


@app.route('/range_numeri')
def esercizio_range():

    start = int(request.args.get('start', default=0))
    stop = int(request.args.get('stop', default=10))

    numeri = range(start, stop)

    return render_template('esercizio1.html', inizio=start, fine=stop, numeri=numeri)




app.run(debug=True)