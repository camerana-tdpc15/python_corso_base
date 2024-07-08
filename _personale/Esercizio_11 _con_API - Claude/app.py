from flask import Flask, request, jsonify, session, render_template
from models import db, User, Prodotto, Produttore, Lotto, Prenotazione, init_db
from settings import DATABASE
from functools import wraps

app = Flask(__name__)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE,
    DEBUG=True)

db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    user = User.query.get(session['user_id'])
    return jsonify(user.to_dict()), 200

@app.route('/api/lotti', methods=['GET'])
def get_lotti():
    lotti = Lotto.query.filter_by(sospeso=False).all()
    lotti_data = []
    for lotto in lotti:
        lotto_dict = lotto.to_dict()
        lotto_dict['quantita_disponibile'] = lotto.quantita_disponibile
        lotto_dict['prodotto'] = lotto.prodotto.to_dict()
        lotti_data.append(lotto_dict)
    return jsonify(lotti_data), 200

@app.route('/api/lotti/<int:id>', methods=['GET'])
def get_lotto(id):
    lotto = Lotto.query.get_or_404(id)
    lotto_dict = lotto.to_dict()
    lotto_dict['quantita_disponibile'] = lotto.quantita_disponibile
    lotto_dict['prodotto'] = lotto.prodotto.to_dict()
    return jsonify(lotto_dict), 200

@app.route('/api/prenotazioni', methods=['GET'])
@login_required
def get_prenotazioni():
    prenotazioni = Prenotazione.query.filter_by(utente_id=session['user_id']).all()
    prenotazioni_data = []
    for p in prenotazioni:
        p_dict = p.to_dict()
        p_dict['lotto'] = p.lotto.to_dict()
        p_dict['lotto']['prodotto'] = p.lotto.prodotto.to_dict()
        prenotazioni_data.append(p_dict)
    return jsonify(prenotazioni_data), 200

@app.route('/api/prenotazioni', methods=['POST'])
@login_required
def create_prenotazione():
    data = request.json
    lotto = Lotto.query.get(data['lotto_id'])
    
    if not lotto or lotto.sospeso:
        return jsonify({'message': 'Lotto non disponibile'}), 400
    
    if data['qta'] > lotto.quantita_disponibile:
        return jsonify({'message': 'Quantità non disponibile'}), 400
    
    existing_prenotazione = Prenotazione.query.filter_by(utente_id=session['user_id'], lotto_id=data['lotto_id']).first()
    if existing_prenotazione:
        return jsonify({'message': 'Prenotazione già esistente per questo lotto'}), 400
    
    prenotazione = Prenotazione(utente_id=session['user_id'], lotto_id=data['lotto_id'], qta=data['qta'])
    db.session.add(prenotazione)
    db.session.commit()
    
    return jsonify(prenotazione.to_dict()), 201

@app.route('/api/prenotazioni/<int:id>', methods=['PUT'])
@login_required
def update_prenotazione(id):
    prenotazione = Prenotazione.query.get(id)
    if not prenotazione or prenotazione.utente_id != session['user_id']:
        return jsonify({'message': 'Prenotazione non trovata'}), 404
    
    data = request.json
    if data['qta'] > prenotazione.lotto.quantita_disponibile + prenotazione.qta:
        return jsonify({'message': 'Quantità non disponibile'}), 400
    
    prenotazione.qta = data['qta']
    db.session.commit()
    
    return jsonify(prenotazione.to_dict()), 200

@app.route('/api/prenotazioni/<int:id>', methods=['DELETE'])
@login_required
def delete_prenotazione(id):
    prenotazione = Prenotazione.query.get(id)
    if not prenotazione or prenotazione.utente_id != session['user_id']:
        return jsonify({'message': 'Prenotazione non trovata'}), 404
    
    db.session.delete(prenotazione)
    db.session.commit()
    
    return jsonify({'message': 'Prenotazione eliminata'}), 200

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)