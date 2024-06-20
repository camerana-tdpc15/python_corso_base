from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
MIO_FILE_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.txt')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        nome = request.form['nome']
        messaggio = request.form['messaggio']
        with open('guestbook.txt', mode='a', encoding='utf-8') as file:
            file.write(f'{nome}: {messaggio} \n')
    
    else: 
     request.method == 'GET'
    with open(MIO_FILE_PATH, mode='r', encoding='utf-8') as file:
        righe = file.readlines()

        risposta= jsonify(righe)

    return risposta

    



if __name__ == '__main__':
    app.run(debug=True)