from flask import Flask, render_template,jsonify
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


@app.route('/api/lotti', methods= ['GET'])
def get_lotti():
    lotti = Lotto.query.all()
    lotti_data = []
    for lotto in lotti :
        dict_lotto=lotto.to_dict()
        lotti_data.append(dict_lotto)
        
     #   prodotto_id = lotto.prodotto_id
     #   prodotto = db.session.get(Prodotto, prodotto_id)
#
     #   produttore= db.session.get(Produttore, prodotto.produttore_id)
     #   data = {              
     #       'id':lotto.id,
     #       'data_consegna':lotto.data_consegna,
     #       'get_date':lotto.get_date(),
     #       'get_qta_disponibile':lotto.get_qta_disponibile(),
     #       'qta_unita_misura':lotto.qta_unita_misura,
     #       'qta_lotto':lotto.qta_lotto,
     #       'prezzo_unitario':lotto.get_prezzo_str(),
     #       'sospeso':lotto.sospeso,
     #       'prodotto':{
     #           'prodotto_nome':prodotto.nome_prodotto,               
     #           'produttore':{
     #               'produttore':produttore.nome_produttore               
     #           }
     #       }
     #   }
     #   lotti_data.append(data)

    return jsonify(lotti_data)


# @TODO: Qua ci vanno le routes
# ...

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)