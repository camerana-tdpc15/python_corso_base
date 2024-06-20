from flask import Flask, request, render_template
import os


BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
MIO_FILE_PATH = os.path.join(BASE_DIR_PATH, 'messaggi_sol02.txt')



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def gestisci_messaggi():
    if request.method == 'POST':
        inputed_message = request.form.get('messaggio')
        if inputed_message:
            with open(MIO_FILE_PATH, 'a') as file:
                file.write(f"{inputed_message}\n")

    with open(MIO_FILE_PATH, 'r') as file:
        messaggi = file.readlines()

    return render_template('home_test09_sol02.html', messaggi=messaggi)

@app.route('/')
def visualizza_messaggi():
    with open(MIO_FILE_PATH, 'r') as file:
        messaggi = file.readlines()

    return render_template('home_test09_sol02.html', messaggi=messaggi)




if __name__ == '__main__':
    app.run(debug=True)
