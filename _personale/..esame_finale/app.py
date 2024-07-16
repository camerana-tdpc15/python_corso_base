from flask import Flask, flash, render_template, jsonify, request, session, redirect, url_for
from models import db, Locale, Evento, Replica, Utente, Prenotazione
from populates_db import init_db
from settings import DATABASE_PATH


app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH,
 
)

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/repliche/<int:evento_id>')

def repliche(evento_id):
    return render_template('repliche.html', evento_id=evento_id)

@app.route('/prenota', methods=['POST'])

def prenota():
    data = request.json
    replica_id = data.get('replica_id')
    quantita = int(data.get('quantita', 1))
    
    replica = Replica.query.get_or_404(replica_id)
    if replica.annullato:
        return jsonify({'error': 'Questa replica è stata annullata.'}), 400
    
    prenotazione = Prenotazione(utente_id=session['user_id'], replica_id=replica_id, quantita=quantita)
    db.session.add(prenotazione)
    db.session.commit()
    
    return jsonify({'message': 'Prenotazione effettuata con successo!'}), 201

@app.route('/api/prenotazioni', methods=['GET', 'POST'])

def api_prenotazioni():
    if request.method == 'GET':
        prenotazioni = Prenotazione.query.filter_by(utente_id=session['user_id']).all()
        prenotazioni_data = []
        for p in prenotazioni:
            prenotazioni_data.append({
                'id': p.id,
                'evento': p.repliche.eventi.nome_evento,
                'locale': p.repliche.eventi.locali.nome_locale,
                'data_ora': p.repliche.eventi.data_ora.strftime('%d-%m-%Y %H:%M'),
                'quantita': p.quantita,
                'annullato': p.repliche.annullato,
                'replica_id': p.replica_id
            })
        return jsonify(prenotazioni_data)
    
    elif request.method == 'POST':
        data = request.json
        action = data.get('action')
        
        if action == 'create':
            replica_id = data.get('replica_id')
            quantita = data.get('quantita', 1)
            
            # Controllo prenotazione esistente
            existing_prenotazione = Prenotazione.query.filter_by(utente_id=session['user_id'], replica_id=replica_id).first()
            if existing_prenotazione:
                return jsonify({'error': 'Hai già una prenotazione per questa replica.'}), 400
            
            replica = Replica.query.get_or_404(replica_id)
            if replica.annullato:
                return jsonify({'error': 'Questa replica è stata annullata.'}), 400
            
            prenotazione = Prenotazione(utente_id=session['user_id'], replica_id=replica_id, quantita=quantita)
            db.session.add(prenotazione)
            db.session.commit()
            
            return jsonify({'message': 'Prenotazione effettuata con successo!'}), 201
        
        elif action == 'update':
            prenotazione_id = data.get('prenotazione_id')
            nuova_quantita = data.get('quantita')
            
            prenotazione = Prenotazione.query.get_or_404(prenotazione_id)
            if prenotazione.utente_id != session['user_id']:
                return jsonify({'error': 'Non sei autorizzato a modificare questa prenotazione.'}), 403
            
            if prenotazione.rel_replica.annullato:
                return jsonify({'error': 'Questa replica è stata annullata.'}), 400
            
            prenotazione.quantita = nuova_quantita
            db.session.commit()
            
            return jsonify({'message': 'Prenotazione aggiornata con successo!'})
        
        elif action == 'delete':
            prenotazione_id = data.get('prenotazione_id')
            prenotazione = Prenotazione.query.get_or_404(prenotazione_id)
            
            if prenotazione.utente_id != session['user_id']:
                return jsonify({'error': 'Non sei autorizzato a cancellare questa prenotazione.'}), 403
            
            db.session.delete(prenotazione)
            db.session.commit()
            
            return jsonify({'message': 'Prenotazione cancellata con successo!'})
        
        else:
            return jsonify({'error': 'Azione non valida'}), 400

@app.route('/prenotazioni')
 
def prenotazioni():
    return render_template('prenotazioni.html')





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # ATTENZIONE: Possiamo usare la password come parametro di ricerca
        #             perché l'abbiamo memorizzata in chiaro (e non come "hash")
        user = Utente.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            # flash('Login riuscito!')
            return redirect(url_for('prenotazioni'))
        else:
            # flash('Credenziali non valide!')
            return redirect(url_for('login'))
    
    elif request.method == 'GET':
        return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    # flash('Logout effettuato con successo!')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)