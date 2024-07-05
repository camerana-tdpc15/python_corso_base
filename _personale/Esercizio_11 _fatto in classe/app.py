from flask import Flask, jsonify, render_template
from models import Lotto, Prodotto, Produttore, db, init_db
from settings import DATABASE_PATH
import locale

locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/lotti', methods=['GET'])
def get_lotti(): 
    lotti = Lotto.query.all()
    lotti_data = []
    # questo è il metodo più manuale e lungo
    for lotto in lotti:
        
        prodotto = db.session.get(Prodotto, lotto.prodotto_id)
        produttore = db.session.get(Produttore, prodotto.produttore_id)
        data = {
            'id': lotto.id,
            'data_consegna': lotto.data_consegna,
            'get_date': lotto.get_date(),
            'qta_unita_misura': lotto.qta_unita_misura,
            'get_qta_disponibile': lotto.get_qta_disponibile(),
            'qta_lotto': lotto.qta_lotto,
            'prezzo_unitario': lotto.prezzo_unitario,
            'sospeso': lotto.sospeso,
            'prodotto': {
                'nome_prodotto': prodotto.nome_prodotto,
                'produttore': {
                    'nome_produttore': produttore.nome_produttore,
                }
            }
        }
        lotti_data.append(data)

    return jsonify(lotti_data)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)