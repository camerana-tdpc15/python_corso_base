from flask import Flask, render_template,request,session,flash,redirect,url_for,jsonify
from models import db, init_db,Lotto,Prodotto,Produttore
from settings import DATABASE_PATH
import locale




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DATABASE_PATH

db.init_app(app)  # Inizializza l'istanza di SQLAlchemy con l'app Flask



locale.setlocale(locale.LC_TIME,'it_IT')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/lotti', methods=['GET'])#non e necesario specificare se e soltanto GET
def get_lotti():

    lotti = Lotto.query.all()


# para serializar una estructura usar una libreria
#proviamo a mano
    lotti_data = []

    for lotto in lotti:
      
        prodotto = db.session.get(Prodotto,lotto.prodotto_id)
        produttore=db.session.get(Produttore,prodotto.produttore_id)

        data = {
            'id':lotto.id,
            'data_consegna':lotto.data_consegna,
            'get_date':lotto.get_date(),
            'get_qta_disponibile':lotto.get_qta_disponibile(),
            'qta_unita_misura':lotto.qta_unita_misura,
            'qta_lotto':lotto.qta_lotto,
            'prezzo_unitario':lotto.prezzo_unitario,
            'sospeso':lotto.sospeso,
            #'prodotto_nome' : prodotto.nome_prodotto => questa e UNA soluzione
            #COSI E PIU LEGIBILE E VA BENE CON QUELLO CHE ABBIAMO FATTO
            'prodotto':{
                'prodotto_nome' : prodotto.nome_prodotto,
                'produttore':{ 
                    'nome_produttore':produttore.nome_produttore}
            }
        }

        lotti_data.append(data)
    
    return jsonify(lotti_data)





# @TODO: Qua ci vanno le routes
# ...

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)