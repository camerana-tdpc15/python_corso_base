from flask import Flask, request, render_template, jsonify, redirect
import os

app = Flask(__name__)

# Ottiene il percorso assoluto della directory del file corrente
BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

# Definisce il percorso completo del file guestbook.txt
GUESTBOOK_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.txt')

# Route per la homepage
@app.route('/')
def home():   
    with open(GUESTBOOK_PATH, mode='r', encoding='utf-8') as file:
        messaggi = file.readlines()
    return render_template('guestbook.html', messaggi=messaggi)
    
# Route per gestire l'aggiunta di nuovi messaggi al guestbook
@app.route('/api/guestbook', methods = ['POST'])
def scrittura():
    if request.method == 'POST':
        nome = request.form.get('nome')
        messaggio = request.form.get('messaggio')
        with open(GUESTBOOK_PATH, mode='a', encoding='utf-8') as file:
            file.write(f'{nome} : {messaggio}\n')
        return redirect('/')   
        

    else:
        with open(GUESTBOOK_PATH, mode='r', encoding='utf-8') as file:
            messaggi = file.readlines()
            
        messaggi_json = jsonify(messaggi)
        return messaggi_json
        


# Avvia l'applicazione Flask in modalità debug
if __name__ == '__main__':
    app.run(debug=True)