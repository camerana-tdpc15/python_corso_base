from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from models import db, init_db, Evento, Replica, Locale, Utente, Prenotazione
from settings import DATABASE_PATH
from functools import wraps
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SECRET_KEY'] = 'mysecretkey'

init_db(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Per favore, effettua il login per accedere a questa pagina.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    eventi = Evento.query.all()
    eventi_data = []
    for evento in eventi:
        repliche_data = []
        for replica in evento.rel_repliche:
            posti_prenotati = db.session.query(func.sum(Prenotazione.quantita)).filter_by(replica_id=replica.id).scalar() or 0
            posti_disponibili = evento.rel_locale.posti - posti_prenotati
            repliche_data.append({
                'id': replica.id,
                'data_ora': replica.data_ora,
                'annullato': replica.annullato,
                'posti_disponibili': posti_disponibili
            })
        eventi_data.append({
            'id': evento.id,
            'nome_evento': evento.nome_evento,
            'locale': evento.rel_locale.nome_locale,
            'repliche': repliche_data
        })
    return render_template('index.html', eventi=eventi_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Utente.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['user_name'] = f"{user.nome} {user.cognome}"
            flash(f'Benvenuto, {session["user_name"]}! Login effettuato con successo.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login fallito. Controlla email e password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Logout effettuato con successo.', 'success')
    return redirect(url_for('index'))

@app.route('/api/repliche/<int:evento_id>')
def get_repliche(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    repliche = []
    for replica in evento.rel_repliche:
        posti_prenotati = db.session.query(func.sum(Prenotazione.quantita)).filter_by(replica_id=replica.id).scalar() or 0
        posti_disponibili = evento.rel_locale.posti - posti_prenotati
        repliche.append({
            'id': replica.id,
            'data_ora': replica.data_ora.strftime('%d-%m-%Y %H:%M'),
            'annullato': replica.annullato,
            'posti_disponibili': posti_disponibili
        })
    return jsonify({
        'nome_evento': evento.nome_evento,
        'locale': evento.rel_locale.nome_locale,
        'luogo': evento.rel_locale.luogo,
        'repliche': repliche
    })

@app.route('/repliche/<int:evento_id>')
@login_required
def repliche(evento_id):
    return render_template('repliche.html', evento_id=evento_id)

@app.route('/prenota', methods=['POST'])
@login_required
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
@login_required
def api_prenotazioni():
    if request.method == 'GET':
        prenotazioni = Prenotazione.query.filter_by(utente_id=session['user_id']).all()
        prenotazioni_data = []
        for p in prenotazioni:
            prenotazioni_data.append({
                'id': p.id,
                'evento': p.rel_replica.rel_evento.nome_evento,
                'locale': p.rel_replica.rel_evento.rel_locale.nome_locale,
                'data_ora': p.rel_replica.data_ora.strftime('%d-%m-%Y %H:%M'),
                'quantita': p.quantita,
                'annullato': p.rel_replica.annullato,
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
@login_required
def prenotazioni():
    return render_template('prenotazioni.html')

if __name__ == '__main__':
    app.run(debug=True)