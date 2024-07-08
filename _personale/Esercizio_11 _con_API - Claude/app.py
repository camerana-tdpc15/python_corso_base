from flask import Flask, request, jsonify, g, session
from flask_restful import Api, Resource
from settings import DATABASE
from models import init_db, db, User, Prodotto, Produttore, Lotto, Prenotazione
from datetime import datetime
from functools import wraps
import hashlib
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
api = Api(app)

app.config.update(
    SECRET_KEY='my_very_secret_key123',
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE,
    DEBUG=True
)

db.init_app(app)

def simple_hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, password):
    return hashed_password == hashlib.sha256(password.encode()).hexdigest()

@app.before_request
def before_request():
    if not hasattr(g, 'initialized'):
        create_default_admin()
        g.initialized = True

def create_default_admin():
    if not User.query.filter_by(email='admin@example.com').first():
        default_admin = User(
            nome='Admin',
            cognome='Default',
            telefono='0000000000',
            email='admin@example.com',
            password=simple_hash_password('adminpass'),
            ruolo='admin'
        )
        db.session.add(default_admin)
        db.session.commit()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or User.query.get(session['user_id']).ruolo != 'admin':
            return {'message': 'Admin privileges required'}, 403
        return f(*args, **kwargs)
    return decorated_function

class Home(Resource):
    def get(self):
        prodotti = Prodotto.query.all()
        prodotti_disponibili = []
        for prodotto in prodotti:
            lotto_disponibile = Lotto.query.filter_by(prodotto_id=prodotto.id, sospeso=0).first()
            prodotti_disponibili.append({
                'prodotto': prodotto.to_dict(),
                'disponibile': lotto_disponibile is not None
            })
        return jsonify(prodotti_disponibili)

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password(user.password, data['password']):
            session['user_id'] = user.id
            return {'message': 'Login successful', 'user': user.to_dict()}
        return {'message': 'Invalid credentials'}, 401

class Logout(Resource):
    def get(self):
        session.pop('user_id', None)
        return {'message': 'Logout successful'}

class Register(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email già registrata'}, 400
        new_user = User(
            nome=data['nome'],
            cognome=data['cognome'],
            telefono=data['telefono'],
            email=data['email'],
            password=simple_hash_password(data['password'])
        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Registrazione effettuata con successo'}

class ProdottoResource(Resource):
    def get(self, prodotto_id):
        prodotto = Prodotto.query.get_or_404(prodotto_id)
        lotti = Lotto.query.filter_by(prodotto_id=prodotto_id, sospeso=False).all()
        totale_disponibile = sum(lotto.qta_lotto for lotto in lotti)
        totale_prenotato = sum(prenotazione.qta for prenotazione in Prenotazione.query.join(Lotto).filter(Lotto.prodotto_id == prodotto_id).all())
        quantita_disponibile = max(totale_disponibile - totale_prenotato, 0)
        prezzi_lotti = [lotto.prezzo_unitario for lotto in lotti]
        prezzo = min(prezzi_lotti) if prezzi_lotti else None
        unita_misura = lotti[0].qta_unita_misura if lotti else 'N/A'
        return {
            'prodotto': prodotto.to_dict(),
            'quantita_disponibile': quantita_disponibile,
            'prezzo': prezzo,
            'unita_misura': unita_misura
        }

    def post(self, prodotto_id):
        if 'user_id' not in session:
            return {'message': 'Login required'}, 401
        data = request.get_json()
        quantita = data['quantita']
        utente_id = session['user_id']
        prodotto = Prodotto.query.get_or_404(prodotto_id)
        lotti = Lotto.query.filter_by(prodotto_id=prodotto_id, sospeso=False).all()
        for lotto in lotti:
            if lotto.qta_lotto >= quantita:
                lotto.qta_lotto -= quantita
                new_prenotazione = Prenotazione(lotto_id=lotto.id, utente_id=utente_id, qta=quantita)
                db.session.add(new_prenotazione)
                db.session.commit()
                return {'message': 'Prenotazione effettuata con successo'}
        return {'message': 'Quantità non disponibile in nessun lotto'}, 400

class CarrelloResource(Resource):
    def get(self):
        if 'user_id' not in session:
            return {'message': 'Login required'}, 401
        utente_id = session['user_id']
        prenotazioni = Prenotazione.query.filter_by(utente_id=utente_id).all()
        prenotazioni_data = [prenotazione.to_dict() for prenotazione in prenotazioni]
        totale = round(sum(p.qta * p.lotto.prezzo_unitario for p in prenotazioni), 2)
        return {'prenotazioni': prenotazioni_data, 'totale': totale}

    def post(self):
        if 'user_id' not in session:
            return {'message': 'Login required'}, 401
        data = request.get_json()
        prenotazione_id = data['prenotazione_id']
        prenotazione = Prenotazione.query.get_or_404(prenotazione_id)
        if prenotazione.utente_id != session['user_id']:
            return {'message': 'Unauthorized'}, 403
        if 'update' in data:
            new_quantity = data['quantita']
            diff = new_quantity - prenotazione.qta
            if prenotazione.lotto.qta_lotto >= diff:
                prenotazione.lotto.qta_lotto -= diff
                prenotazione.qta = new_quantity
                db.session.commit()
                return {'message': 'Quantità aggiornata con successo'}
            return {'message': 'Quantità non disponibile'}, 400
        elif 'delete' in data:
            prenotazione.lotto.qta_lotto += prenotazione.qta
            db.session.delete(prenotazione)
            db.session.commit()
            return {'message': 'Prodotto rimosso con successo'}

class NuovoProduttoreResource(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        nuovo_produttore = Produttore(
            nome_produttore=data['nome_produttore'],
            descrizione=data['descrizione'],
            indirizzo=data['indirizzo'],
            telefono=data['telefono'],
            email=data['email']
        )
        db.session.add(nuovo_produttore)
        db.session.commit()
        return {'message': 'Produttore aggiunto con successo'}

class NuovoProdottoResource(Resource):
    @admin_required
    def get(self):
        produttori = Produttore.query.all()
        return {'produttori': [produttore.to_dict() for produttore in produttori]}

    @admin_required
    def post(self):
        data = request.get_json()
        nuovo_prodotto = Prodotto(
            produttore_id=data['produttore_id'],
            nome_prodotto=data['nome_prodotto'],
            image_url=data['image_url']
        )
        db.session.add(nuovo_prodotto)
        db.session.commit()
        return {'message': 'Prodotto aggiunto con successo'}

class NuovoLottoResource(Resource):
    @admin_required
    def get(self):
        prodotti = Prodotto.query.all()
        return {'prodotti': [prodotto.to_dict() for prodotto in prodotti]}

    @admin_required
    def post(self):
        data = request.get_json()
        nuovo_lotto = Lotto(
            prodotto_id=data['prodotto_id'],
            data_consegna=datetime.strptime(data['data_consegna'], '%Y-%m-%d'),
            qta_unita_misura=data['qta_unita_misura'],
            qta_lotto=data['qta_lotto'],
            prezzo_unitario=data['prezzo_unitario'],
            sospeso=data['sospeso']
        )
        db.session.add(nuovo_lotto)
        db.session.commit()
        return {'message': 'Lotto aggiunto con successo'}

class GestisciUtentiResource(Resource):
    @admin_required
    def get(self):
        utenti = User.query.all()
        return {'utenti': [utente.to_dict() for utente in utenti]}

    @admin_required
    def post(self):
        data = request.get_json()
        utente = User.query.get_or_404(data['user_id'])
        utente.ruolo = data['ruolo']
        db.session.commit()
        return {'message': 'Ruolo aggiornato con successo'}

api.add_resource(Home, '/')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Register, '/registrazione')
api.add_resource(ProdottoResource, '/prodotto/<int:prodotto_id>')
api.add_resource(CarrelloResource, '/carrello')
api.add_resource(NuovoProduttoreResource, '/nuovo_produttore')
api.add_resource(NuovoProdottoResource, '/nuovo_prodotto')
api.add_resource(NuovoLottoResource, '/nuovo_lotto')
api.add_resource(GestisciUtentiResource, '/gestisci_utenti')

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)