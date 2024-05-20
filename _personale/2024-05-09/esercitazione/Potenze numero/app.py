from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculate_powers():
    if request.method == 'POST':
        try:
            number = float(request.form['number'])
            powers = [number**i for i in range(4)]
        except ValueError:
            number = None
            powers = []
        return render_template('index.html', number=number, powers=powers)
    else:
        return render_template('index.html', number=None, powers=[])

if __name__ == '__main__':
    app.run(debug=True)