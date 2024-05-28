from flask import Flask, request, render_template

app = Flask(__name__)

    #http://127.0.0.1:5000/potenze

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

# Avvia direttamente l'applicazione in modalità debug.
app.run()
