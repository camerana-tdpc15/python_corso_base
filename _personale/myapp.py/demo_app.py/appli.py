from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/range_numeri')
def esercizio_range():
    start = request.args.get('start')
    stop = request.args.get('start')
    numeri = range(start, stop)
    print(numeri)
    return render_template('esercizio.html', start=start, stop=stop)


app.run(debug=True)