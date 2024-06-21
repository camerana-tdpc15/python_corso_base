from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import os

app = Flask(__name__)

BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
MIO_FILE_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.txt')


@app.route('/')
def home():   

    return render_template('guestbook.html')


@app.route('/api/guestbook', methods = ['POST'])
def scrittura():
    if request.method == 'POST':
        nome = request.form['nome']
        messaggio = request.form['messaggio']

        with open(MIO_FILE_PATH, mode='a', encoding='utf-8') as file:
            file.write(f'{nome} : {messaggio}\n')
       

    else:
        with open('guestbook.txt', mode='r', encoding='utf-8') as file:
            messaggi = file.readlines()
            
        messaggi_json = jsonify(messaggi)
        return messaggi_json
        



if __name__ == '__main__':
    app.run(debug=True)