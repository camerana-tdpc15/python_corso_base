from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():

    esercizi_list = [
        ('Esercizio1', '/range_numeri'),
        ('index', '/index')
    ]
    return render_template('index.html', esercizi=esercizi_list)


@app.route("/range_numeri")
def func_esercizio1():

    inizio =  int(request.args.get('varin1', default=0))
    fine =  int(request.args.get('varin2', default=10))

    lista = range(inizio, fine)
    print(request.args)

    return render_template('esercizio1.html', primo=inizio, ultimo=fine, varout=lista)



    

    



app.run(debug=True)