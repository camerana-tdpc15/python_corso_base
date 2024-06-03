from flask import Flask, request, jsonify

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

@app.route('/calculate', methods=['POST'])
def calculate_route():
    data = request.json
    number1 = data['number1']
    number2 = data['number2']
    operator = data['operator']
    result = calculate(number1, number2, operator)
    return jsonify(result=result)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
