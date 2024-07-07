import locale

from pprint import pprint
from flask import Flask, render_template, jsonify

# qui importo il db da models
from settings import DATABASE_PATH
from models import Lotto, Prodotto, Produttore, db, init_db


locale.setlocale(locale.LC_TIME, 'it_IT')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH

# qui inizializzo il db importato da models
db.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')

# creo un end point per poter visualizzare tutti i lotti
@app.route('/api/get_lotti', methods=['GET'])

# creo funzione per ottenere lotti
def get_lotti():
    lotti = Lotto.query.all()

    # lotti_data = []

    # for lotto in lotti:

    #     prodotto_id = lotto.prodotto_id
        
    #     prodotto = db.session.get(Prodotto, lotto.prodotto_id)
    #     produttore = db.session.get(Produttore, prodotto.produttore_id)
    #     data = {
    #         'id': lotto.id,
    #         'data_consegna':lotto.data_consegna,
    #         'get_date': lotto.get_date(),
    #         'get_qta_disponibile': lotto.get_qta_disponibile(),
    #         'qta_unita_misura':lotto.qta_unita_misura,
    #         'qta_lotto':lotto.qta_lotto,
    #         'prezzo_unitario':lotto.prezzo_unitario,
    #         'sospeso':lotto.sospeso,
    #         'prodotto':{
    #             'nome_prodotto':prodotto.nome_prodotto,
    #             'produttore':{
    #                 'nome_produttore':produttore.nome_produttore
    #             }
    #         }
    #     }
    #     lotti_data.append(data)

    lotti_data = []
    for lotto in lotti:
        dict_lotto = lotto.to_dict()
        lotti_data.append(dict_lotto)
    
    return jsonify(lotti_data)

    

if __name__ == '__main__':
    # con il contesto dell'app esistente
    with app.app_context():

        # avvio la funzione per inizializzare l'app
        init_db(app)

    app.run(debug=True)