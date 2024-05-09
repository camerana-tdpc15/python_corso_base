from flask import Flask, request

app = Flask(__name__)

@app.route('/range_numeri')
def esercizio_range():
    start =request.args.get('start')
    stop =request.args.get('stop')
    numeri = range(start, stop)

app.run(debug=True)