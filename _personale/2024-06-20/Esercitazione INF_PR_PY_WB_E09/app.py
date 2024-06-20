from flask import Flask, jsonify, render_template, request
import os

BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
MIO_FILE_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.txt')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('guestbook.html')

@app.route('/api/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        name = request.json.get('nome')
        message = request.json.get('messaggio')
        if not name or not message:
            response = {'error': 'Nome e messaggio sono obbligatori'}
            return jsonify(response)
        
        with open(MIO_FILE_PATH, mode='a', encoding='utf-8') as file:
            file.write('Nome: Messaggio\n')
            response = {'success': 'ok'}
            return jsonify(response)
    
    else:
        ...
    
       



@app.route('/guestbook', methods=['GET'])
def index():
    return render_template('guestbook.html')

if __name__ == '__main__':
    app.run(debug=True)