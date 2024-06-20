from flask import Flask, request, render_template
import os


BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
MIO_FILE_PATH = os.path.join(BASE_DIR_PATH, 'messaggi.txt')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def gestisci_messaggi():
    if request.method == 'POST':
        messaggio = request.form.get('messaggio')
        with open(MIO_FILE_PATH, 'a') as file:
            file.write(f"{messaggio}\n")

    with open(MIO_FILE_PATH, 'r') as file:
        messaggi = file.readlines()

    return render_template('home_test09.html', messaggi=messaggi)

if __name__ == '__main__':
    app.run(debug=True)