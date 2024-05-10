from flask import Flask, request, render_template

app = Flask (__name__)   
@app.route('/ESERCIZIO_01_range_numeri')

def esrcizio_range():
    start= request.args.get('start')
    stop= request.args.get('stop')
    numeri = range(start, stop)
    return render_template('Esercizio_01',start = start, stop = stop)

print (numeri)



app.run(debug=True)