from flask import Flask, render_template, request
from datetime import date, timedelta
import locale

# Imposta la localizzazione italiana
locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)

@app.route('/')
def home():
    esercizi_list = [
        ('Esercizio 1', '/number_range'),
        ('Esercizio 2', '/powers'),
        ('Esercizio 3', '/dates'),
        ('Esercizio 4', '/string_table')
    ]
    return render_template('index_bs.html', esercizi=esercizi_list)


@app.route('/number_range', methods=['GET', 'POST'])
def number_range():
    # Definisco i default
    numbers = []
    start = 0
    stop = 10
    if request.method == 'POST':
        start = int(request.form.get('start') or start)
        stop = int(request.form.get('stop') or stop)
        if start <= stop:
            numbers = list(range(start, stop+1))
        else:
            numbers = list(range(start, stop-1, -1))
    # In caso invece che la chiamata sia di tipo GET
    else:
        # Non fare nulla
        pass

    return render_template('number_range_bs.html', number_list=numbers, start=start, stop=stop)


@app.route('/powers', methods=['GET', 'POST'])
def powers():
    number = 2  # Default number to avoid errors in calculations if not posted
    powers = {}
    if request.method == 'POST':
        number = int(request.form.get('number', 2))
        powers = {i: number**i for i in range(2, 6)}
    
    return render_template('powers_bs.html', base_number=number, powers=powers)


@app.route('/dates', methods=['GET', 'POST'])
def dates():
    date_list = []
    if request.method == 'POST':
        today = date.today()
        date_list =  [(today + timedelta(days=2*i)).strftime("%A %d/%m/%Y") for i in range(6)]
    return render_template('dates_bs.html', date_list=date_list)


@app.route('/string_table', methods=['GET', 'POST'])
def string_table():
    string1 = request.form.get('string1', '')
    string2 = request.form.get('string2', '')
    results = {
        'string1': string1,
        'string2': string2,
        'concat_1_2': string1 + ' ' + string2,
        'concat_2_1': string2 + ' ' + string1,
        'initials': (string1 and string1[0]) + (string2 and string2[0]),
        # 'initials': (string1[0] if string1 else '') + (string2[0] if string2 else ''),
        # 'initials': ''.join([s[0] for s in string1.split()] + [s[0] for s in string2.split()]),
        'reverse_string1': string1[::-1]
    }
    return render_template('string_table_bs.html', results=results)


# Controlla se questo file Python è stato eseguito come script
if __name__ == '__main__':
    # Sono sicuro che l'applicazione è stata avviata come script
    # e dunque il server va avviato.
    app.run(debug=True)
