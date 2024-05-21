from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Visualizza il form vuoto all'inizio
        return render_template('index.html')

    elif request.method == 'POST':
        # Ottenere i valori dal form
        start_num = int(request.form['start_num'])
        end_num = int(request.form['end_num'])

        # Generare la lista di numeri
        numbers_list = list(range(start_num, end_num + 1))

        # Rendere il template con la lista
        return render_template('index.html', numbers_list=numbers_list)

if __name__ == '__main__':
    app.run(debug=True)
