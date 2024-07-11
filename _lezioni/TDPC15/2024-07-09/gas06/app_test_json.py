import locale
from flask import Flask, render_template, jsonify
from models import db, init_db, Lotto, Prodotto, Produttore
from settings import DATABASE_PATH

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

    for lotto in lotti:
        # Se vogliamo sfruttare le relationship che abbiamo creato
        # possiamo sfruttare la notazione a punti!
        prodotto = lotto.rel_prodotto
        produttore = prodotto.rel_produttore

        # Se non abbiamo le relazioni oppure vogliamo usare eplicitamente
        # il .get() per ottenere il record:
        # prodotto = db.session.get(Prodotto, lotto.prodotto_id)
        # produttore = db.session.get(Produttore, prodotto.produttore_id)

        data = {
            'id': lotto.id,
            'data_consegna': lotto.data_consegna,
            'get_date': lotto.get_date(),  # es. "Giovedì 27/06/2024"
            'get_prezzo_str': lotto.get_prezzo_str(),  # es. "8.50 €/L"
            'get_qta_disponibile': lotto.get_qta_disponibile(), # es. 94
            'qta_unita_misura': lotto.qta_unita_misura,
            'qta_lotto': lotto.qta_lotto,
            'prezzo_unitario': lotto.prezzo_unitario,
            'sospeso': lotto.sospeso,
            'prodotto_id': lotto.prodotto_id,
            'prodotto': {
                'nome_prodotto': prodotto.nome_prodotto,
                'produttore': {
                    'nome_produttore': produttore.nome_produttore
                }
            }
        }

        lotti_data.append(data)
    
    return jsonify(lotti_data)


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)