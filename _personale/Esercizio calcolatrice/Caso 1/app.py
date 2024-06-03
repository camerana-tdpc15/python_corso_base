from flask import Flask, render_template, request

app = Flask(__name__)

def calculate(number1, number2, operator):
    if operator == 'add':
        return number1 + number2
    elif operator == 'subtract':
        return number1 - number2
    elif operator == 'multiply':
        return number1 * number2
    elif operator == 'divide':
        return number1 / number2

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        number1 = float(request.form['number1'])
        number2 = float(request.form['number2'])
        operator = request.form['operator']
        result = calculate(number1, number2, operator)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
