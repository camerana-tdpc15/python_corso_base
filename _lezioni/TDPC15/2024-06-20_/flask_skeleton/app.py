from flask import Flask, request, jsonify

app = Flask(...)

@app.route('/api/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        # Lettura di nome e messaggio
        nome = ...
        messaggio = ...
        if not nome or not messaggio:
            response = {'error': 'Nome e messaggio sono obbligatori!'}
            return jsonify(response)
        # Scrittura su file
        ... # with open ... as :
        respose = {'success': 'ok'}
        return jsonify(response)
    else:  # richiesta GET
        # Lettura del file
        # Restituzione delle righe del file in formato JSON
        ...