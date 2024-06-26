from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


BASE_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
#percorso del file di database
DATABASE_PATH = os.path.join(BASE_DIR_PATH, 'guestbook.db')
#utilizzo sqlAlchemy come motore di database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
#disabilito il monitoraggio automatico delle modifiche
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modello per i messaggi del guestbook
class GuestbookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)

# Creare il database e le tabelle se non esistono
with app.app_context():
    db.create_all()

# Route per la pagina HTML
@app.route('/')
def guestbook():
    return render_template('guestbook.html')

# Route per l'API
@app.route('/api/guestbook', methods=['GET', 'POST'])
def api_guestbook():
    if request.method == 'POST':
        # Aggiungere un nuovo messaggio
        name = request.json.get('name')
        message = request.json.get('message')
        if name and message:
            new_entry = GuestbookEntry(name=name, message=message)
            db.session.add(new_entry)
            db.session.commit()
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid input'}), 400
    elif request.method == 'GET':
        # Leggere tutti i messaggi dal più recente
        entries = GuestbookEntry.query.order_by(GuestbookEntry.id.desc()).all()
        messages = [{'name': entry.name, 'message': entry.message} for entry in entries]
        return jsonify(messages), 200

if __name__ == '__main__':
    app.run(debug=True)
