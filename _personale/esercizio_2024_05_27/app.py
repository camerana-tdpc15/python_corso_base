from datetime import date, timedelta
from Flask import Flask, request, render_template
app= Flask(__name__)

# Questa route risponde a un questo URL:
# http://127
@app.route('/potenza')
def esercizio_potenza(:
numero = int(request.args.get('base_number', default=2))
# print('Numero ricevuto:', numero)
potenze = {}
for esponente in range(2,6):
potenze[esponente] = numero ** esponente


potenze = {esponente: numero ** esponente for esponente in range(2,6)}
print (potenze)
return render_template('esercizio2.html', power=potenze, submitted_number=numero);

# Avvia direttamente


@app.route('/date')
def esercizio_date():
lista_date = []
oggi = date.today() 
for num in range(6):
    data = oggi + timedelta(days=2*num)
    lista_date.append(data.strftime('%A %d/ %m/%Y'))
    print(lista_date)


return render_template('esercizio3.html', lista_date=lista_date)