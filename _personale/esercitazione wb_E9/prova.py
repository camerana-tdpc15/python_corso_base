from flask import Flask, render_template,request,jsonify


app = Flask(__name__)




@app.route('/', methods=['GET'])
def visualizza_guestbook():
    # Leggi i messaggi dal file di testo
    with open('guestbook.txt', 'a') as file:
        messaggi = file.readlines()
    return render_template('guestbook.html', messaggi=messaggi)

# Endpoint per l'invio di un nuovo messaggio
@app.route('/api/guestbook', methods=['POST'])
def invia_messaggio():
    nome = request.form.get('nome')
    messaggio = request.form.get('messaggio')
    if nome and messaggio:
        # Salva il messaggio nel file di testo
        with open('guestbook.txt', 'a') as file:
            file.write(f"{nome}: {messaggio}\n")
        return jsonify({"success": True, "message": "Messaggio aggiunto con successo!"})
    else:
        return jsonify({"success": False, "message": "Nome e messaggio sono obbligatori."})


if __name__ == '__main__':
    app.run(debug=True)